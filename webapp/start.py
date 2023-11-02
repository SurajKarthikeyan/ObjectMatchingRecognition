from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'whole' in request.files and 'part' in request.files:
        whole = request.files['whole']
        part = request.files['part']
        if whole:
            wholename = secure_filename(whole.filename)
            wholepath = os.path.join(app.config['UPLOAD_FOLDER'], wholename)
            whole.save(wholepath)
        if part:
            partname = secure_filename(part.filename)
            partpath = os.path.join(app.config['UPLOAD_FOLDER'], partname)
            part.save(partpath)
        return render_template('display.html', whole_filename=wholename, part_filename=partname)

if __name__ == '__main__':
    app.run(debug=True)