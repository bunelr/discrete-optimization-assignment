from flask import Flask, render_template, request
from flaskext.uploads import configure_uploads, patch_request_class, UploadSet, UploadNotAllowed
from flask.ext.basicauth import BasicAuth
import shutil
import os
import zipfile

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


        return render_template('ok.html')
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
        c_ressources_dir = os.path.join(app.config['ressources'], 'c')
        for f in c_files:
            shutil.copyfile(os.path.join(c_ressources_dir, f), os.path.join(work_directory,f))
    elif lang == 'python':
        python_files  = ['run.sh']
        python_ressources_dir = os.path.join(app.config['ressources'], 'python')
        for f in python_files:
            shutil.copyfile(os.path.join(python_ressources_dir, f), os.path.join(work_directory,f))

    common_ressources_dir = os.path.join(app.config['ressources'], 'common')
    common_files = ['metroEdgeDist.txt', 'testResults.py']
    for f in python_files:
        shutil.copyfile(os.path.join(common_ressources_dir, f), os.path.join(work_directory,f))



if __name__ == '__main__':
    app.run(debug=True)
