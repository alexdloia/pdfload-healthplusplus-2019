import os, json
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def hello_world():
    return render_template("index.html")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/pdf_upload', methods=['GET', 'POST'])
def get_pdf():
    context = dict()
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = 'medrecord.pdf'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            context["success"] = True
    return render_template("pdf_upload.html", **context)


@app.route('/get_file', methods=['POST'])
def get_file():
    data = dict()
    with open('medrecord.txt') as f:
        data['data'] = f.read()
    return render_template('get_file.html', data_str=json.dumps(data))

@app.route('/web_form')
def web_form():
    return render_template('web_form.html')
