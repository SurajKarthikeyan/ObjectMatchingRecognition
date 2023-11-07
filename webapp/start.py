from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os
from BASNet import *

# Initial Setup
app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

"""
Starting function
Takes nothing
Loads home page
"""

@app.route('/')
def index():
    bas_start()
    return render_template('upload.html')


"""
Runs on call to generate
Takes request.files with (potentially) 'whole' and 'part'
Loads upload.html
"""
@app.route('/upload', methods=['POST'])
def upload_file():
    # unpacks request.files
    if 'whole' in request.files and 'part' in request.files:
        whole = request.files['whole']
        part = request.files['part']

        # If both images have been uploaded
        if whole and part:
            wholename = secure_filename(whole.filename)
            wholepath = os.path.join(app.config['UPLOAD_FOLDER'], wholename)
            whole.save(wholepath)

            partname = secure_filename(part.filename)
            partpath = os.path.join(app.config['UPLOAD_FOLDER'], partname)
            part.save(partpath)

            partbas = data_handle(partname)


            return render_template('display.html', whole_filename=wholename, part_filename=partname)

        # At least one of the images hasn't been uploaded
        else:
            return render_template('no_image.html')

if __name__ == '__main__':
    app.run(debug=True)