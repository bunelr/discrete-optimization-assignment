from flask import Flask, render_template, request
from flaskext.uploads import configure_uploads, patch_request_class, UploadSet, UploadNotAllowed
from flask.ext.basicauth import BasicAuth
import shutil
import os
import zipfile
import subprocess
import json

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

        work_directory = unzip(user_folder, filename)

        lang = request.form['lang']

        provide_ressources(work_directory, lang)

        return_code = do_the_run(work_directory)

        if return_code != 0:
            return handle_bad(return_code, work_directory)
        else:
            return handle_good(work_directory, username, filename)


    elif(request.method == 'GET'):
        return render_template('submit.html')
    else:
        return render_template('fuck_up.html', reason='Your submission is missing something')


def unzip(folder, filename):
    zip_file = os.path.join(folder, filename)
    user_dir = os.path.dirname(zip_file)
    with zipfile.ZipFile(zip_file, "r") as z:
        z.extractall(user_dir)
    content = os.listdir(user_dir)
    container = [name for name in content if not name.endswith('.zip')][0]
    return os.path.join(user_dir, container)

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
    common_files = ['metroEdgeDist.txt', 'testResults.py']
    for f in common_files:
        shutil.copy2(os.path.join(common_ressources_dir, f), os.path.join(work_directory,f))


def do_the_run(work_dir):
    # Do it by printing
    p = subprocess.Popen(['/bin/bash', 'run.sh', '1'], cwd = work_dir)
    return p.wait()


def handle_bad(return_code):
    reasons = {1: "Could not build with the print flag on",
               2: "Could not build with the print flag off",
               3: "Results are incorrect",
               4: "The programm errored while running with the print flag on",
               5: "The program errored while running with the print flag off"}
    return render_template('fuck_up.html', reason=reasons[return_code])


def handle_good(work_directory, username, filename):
    runtime_file = os.path.join(work_directory, 'runtime.txt')
    with open(runtime_file,'r') as rf:
        runtime = rf.read()

    results = get_values(runtime)
    key = "-".join([username, filename])

    with open(app.config['HALL_OF_FAME'], 'r') as hall_of_fame:
        hall = json.load(hall_of_fame)

    hall_of_fame[key] = results

    with open(app.config['HALL_OF_FAME'], 'w') as hall_of_fame:
        hall = json.dump(hall_of_fame)


    return render_template('ok.html', runtime = runtime)

def get_values(runtime_txt):
    lines = runtime_txt.splitlines()
    dij = float(lines[0].split()[1])
    bel = float(lines[1].split()[1])
    flo = float(lines[2].split()[1])
    return {"dij" : dij,
            "bel" : bel,
            "flo" : flo}


if __name__ == '__main__':
    app.run(debug = True, use_reloader = False)
