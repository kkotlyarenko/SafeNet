import os
import analyse
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "C:/Users/somet/PycharmProjects/flaskProject"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def main_page():
    return render_template('mainpage.html')

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    try:
        if request.method == 'POST':
            f = request.files['file']
            f.save(secure_filename(f.filename))
            context = [x for x in analyse.checkQR(f.filename).split('\n')]
            os.remove(f.filename)
            return render_template('txtupload.html', context=context)
    except:
        return render_template('mainpage.html')
@app.route('/txtuploader', methods=['GET', 'POST'])
def upload_txt():
    try:
        if request.method == 'POST':
            f = request.form['text']
            context = [x for x in analyse.checkURL(f).split('\n')]

            return render_template('txtupload.html', context=context)
    except:
        return render_template('mainpage.html')


if __name__ == '__main__':
    app.run(debug=True)
