from flask import Flask, render_template, request
from flaskext.uploads import configure_uploads, patch_request_class, UploadSet, UploadNotAllowed
from flask.ext.basicauth import BasicAuth
import shutil
import os
import zipfile
import subprocess
import json
from statsd import statsd

from werkzeug import secure_filename

LOCAL_ARCHIVE_NAME = 'code.zip'

app = Flask(__name__)
app.config.from_object('config.Config')

archives = UploadSet(extensions=['zip'], default_dest = lambda app: app.config['SUBMISSION_FOLDER'])

configure_uploads(app, archives)
patch_request_class(app, size = 5*1024*1024)

basic_auth = BasicAuth(app)

@app.route('/submit', methods=['GET', 'POST'])
@basic_auth.required
def upload():
    if (request.method == 'POST') and \
       ('code' in request.files) and \
       ('username' in request.form) and \
       (request.files['code'].filename != '') and \
       (request.form['username']!= '') and \
       (request.form['lang'] in ['C','python']):


        try:
            username = request.form['username']
            clean_path = secure_filename(username)
            filename = archives.save(request.files['code'], folder=clean_path, name=LOCAL_ARCHIVE_NAME)
        except UploadNotAllowed:
            return render_template('fuck_up.html', reason="Problem with the upload")

        user_folder = app.config['SUBMISSION_FOLDER']

        try:
            work_directory = unzip(user_folder, filename)
        except Exception as e:
            clean_files(user_folder)
            return render_template('fuck_up.html', reason="Your zip file is not formatted correcly, check the submit page")

        lang = request.form['lang']

        provide_ressources(work_directory, lang)

        return_code, out, err = do_the_run(work_directory)

        statsd.increment('assignment.submission',tags=["result:"+str(return_code),"lang:"+lang])
        if return_code != 0:
            return handle_bad(return_code,out, err, work_directory)
        else:
            return handle_good(work_directory, username, filename)


    elif(request.method == 'GET'):
        statsd.increment('page.views',tags=["page:submit"])
        return render_template('submit.html')
    else:
        statsd.increment('page.views',tags=["page:bad_upload"])
        return render_template('fuck_up.html', reason='Your submission is missing something')

@app.route('/halloffame', methods=['GET'])
@basic_auth.required
def hall_of_fame():
    statsd.increment('page.views',tags=["page:halloffame"])
    with open(app.config['HALL_OF_FAME'], 'r') as hall_of_fame:
        hall = json.load(hall_of_fame)

    halls = [item for item in hall.iteritems()]
    halls.sort(key = lambda it :it[1]['dij'])
    statsd.gauge('assignment.submission_nb', len(halls))
    return render_template('hall_of_fame.html', hall = halls)

def unzip(folder, filename):
    zip_file = os.path.join(folder, filename)
    user_dir = os.path.dirname(zip_file)
    with zipfile.ZipFile(zip_file, "r") as z:
        z.extractall(user_dir)
    content = os.listdir(user_dir)
    containers = [name for name in content if (not name.endswith('.zip') and not name=='__MACOSX')]
    if len(containers)==1 and os.path.isdir(os.path.join(user_dir, containers[0])):
        return os.path.join(user_dir, containers[0])
    else:
        raise Exception('Bad submission.')

def provide_ressources(work_directory, lang):
    if lang == 'C':
        c_files = ['Makefile', 'run.sh']
        c_ressources_dir = os.path.join(app.config['RESSOURCE_FOLDER'], 'c')
        for f in c_files:
            shutil.copy2(os.path.join(c_ressources_dir, f), os.path.join(work_directory,f))
    elif lang == 'python':
        python_files  = ['run.sh']
        python_ressources_dir = os.path.join(app.config['RESSOURCE_FOLDER'], 'python')
        for f in python_files:
            shutil.copy2(os.path.join(python_ressources_dir, f), os.path.join(work_directory,f))

    common_ressources_dir = os.path.join(app.config['RESSOURCE_FOLDER'], 'common')
    common_files = ['metroEdgeDist.txt', 'testResults.py', 'groundTruth.txt']
    for f in common_files:
        shutil.copy2(os.path.join(common_ressources_dir, f), os.path.join(work_directory,f))


def do_the_run(work_dir):
    # Do it by printing
    p = subprocess.Popen(['/bin/bash', 'run.sh', '1'], cwd = work_dir, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    out, err =  p.communicate()
    out = out.decode('utf-8').strip()
    err = err.decode('utf8').strip()
    return_code = p.returncode

    return return_code, out, err

def handle_bad(return_code, out, err, work_directory):
    reasons = {1: "Could not build with the print flag on",
               2: "Could not build with the print flag off",
               3: "Results are incorrect",
               4: "The programm errored while running with the print flag on",
               5: "The program errored while running with the print flag off",
               6: "No runtime.txt file was created"}
    clean(work_directory)
    return render_template('fuck_up.html', reason=reasons[return_code], out = out, err = err)


def handle_good(work_directory, username, filename):

    try:
        runtime_file = os.path.join(work_directory, 'runtime.txt')
        with open(runtime_file,'r') as rf:
            runtime = rf.read()
    except:
        return handle_bad(6, "","",work_directory)
    results = get_values(runtime)
    key = "-".join([username, filename])

    with open(app.config['HALL_OF_FAME'], 'r') as hall_of_fame:
        hall = json.load(hall_of_fame)

    hall[key] = results

    with open(app.config['HALL_OF_FAME'], 'w') as hall_of_fame:
        json.dump(hall, hall_of_fame)

    clean(work_directory)
    return render_template('ok.html', runtime = runtime)

def get_values(runtime_txt):
    lines = runtime_txt.splitlines()
    dij = float(lines[0].split()[1])
    bel = float(lines[1].split()[1])
    flo = float(lines[2].split()[1])
    return {"dij" : dij,
            "bel" : bel,
            "flo" : flo}

def clean(work_directory):
    shutil.rmtree(work_directory)

def clean_files(user_dir):
    content = os.listdir(user_dir)
    content = [f for f in content if not f.endswith('.zip')]
    for f in content:
        p = os.path.join(user_dir, f)
        if os.path.isfile(p):
            os.remove(p)
        elif os.path.isdir(p):
            shutil.rmtree(p)


if __name__ == '__main__':
    app.run(debug = True, use_reloader = False, port=8000)
