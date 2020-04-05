import os
#import magic
import urllib.request
from app import app
from flask import Flask, flash, request, redirect, render_template, send_file
from werkzeug.utils import secure_filename
from pdf_parser import parse_pdf_to_csv

ALLOWED_EXTENSIONS = ['pdf']

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/', methods=['GET'])
def upload_form():
	return render_template('upload.html')

@app.route('/parse', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No file selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('File successfully uploaded')
        parse_pdf_to_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('File successfully parsed.')
        return redirect('/download')
    else:
        flash('Allowed file type is pdf only.')
        return redirect(request.url)

@app.route('/download', methods=['GET'])
def download_file():
    return send_file('../parsed_csv/parsed.csv', as_attachment=True)

if __name__ == "__main__":
    app.run()