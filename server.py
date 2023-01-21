import os
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename


app = Flask(__name__)
UPLOAD_FOLDER = './audio/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['mp3', 'wav', 'ogg'])
not_allowed_extension = 0
uploaded_files = [f for f in os.listdir(UPLOAD_FOLDER)
                  if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]


def run_server():
    app.run(host="localhost", port=8888, debug=True)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    not_allowed_extension = 0
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            not_allowed_extension = 0
            filename = secure_filename(file.filename)
            uploaded_files.append(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            not_allowed_extension = 1
    return render_template("main_page.html", uploaded_files=uploaded_files,
                           not_allowed_extension=not_allowed_extension)


if __name__ == "__main__":
    run_server()
