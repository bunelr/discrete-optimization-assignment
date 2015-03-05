from flask import Flask, render_template, request
from flaskext.uploads import configure_uploads, patch_request_class, UploadSet, UploadNotAllowed
from werkzeug import secure_filename


app = Flask(__name__)
app.config.from_object('config.Config')

archives = UploadSet(extensions=['zip'], default_dest = lambda app: app.config['SUBMISSION_FOLDER'])

configure_uploads(app, archives)
patch_request_class(app, size = 5*1024*1024)

@app.route('/submit', methods=['GET', 'POST'])
def upload():
    if (request.method == 'POST') and \
       ('code' in request.files) and \
       ('username' in request.form) and \
       (request.files['code'].filename != '') and \
       request.form['username']!= '':
        try:
            username = request.form['username']
            clean_path = secure_filename(username)
            filename = archives.save(request.files['code'], folder=clean_path, name='code.zip')
        except UploadNotAllowed:
            return render_template('fuck_up.html', reason="Problem with the upload")


        return render_template('ok.html')
    elif(request.method == 'GET'):
        return render_template('submit.html')
    else:
        return render_template('fuck_up.html', reason='Your submission is missing something')

if __name__ == '__main__':
    app.run(debug=True)
