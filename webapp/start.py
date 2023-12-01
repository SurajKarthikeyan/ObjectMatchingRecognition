from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os
from BASNet import *
from KeypointMatch import *

from config import *

# Initial Setup
app = Flask(__name__)

UPLOAD_FOLDER = path_control + 'uploads'
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
    if 'whole' in request.files:
        whole = request.files['whole']
        part = Image.open(path_control + 'uploads/cropped_image.jpg')
        # If both images have been uploaded
        if whole and part:
            wholename = secure_filename(whole.filename)
            wholepath = os.path.join(app.config['UPLOAD_FOLDER'], wholename)
            whole.save(wholepath)

            partname = secure_filename(part.filename)
            partpath = os.path.join(app.config['UPLOAD_FOLDER'], partname)
            part.save(partpath)

            # this line runs basnet
            baspath = data_handle(partname)

            # to do without basnet, pass in partpath instead of baspath
            match_path = add_matching(path_control+baspath, wholepath)
            print(match_path, wholepath)
            print(baspath, partpath)
            return render_template('display.html', whole_filename=match_path, part_filename='uploads/cropped_image.jpg')

        # At least one of the images hasn't been uploaded
        else:
            return render_template('no_image.html')

@app.route('/save_cropped_image', methods=['POST'])
def save_cropped_image():
    cropped_image = request.files['cropped_image']
    # resize image here
    #resized_img = scale_image(cropped_image, 500, 500)
    # Save the cropped image to the server's file system
    cropped_image.save(os.path.join('static/uploads', 'cropped_image.jpg'))

    return 'Cropped image saved successfully!'

if __name__ == '__main__':
    app.run(debug=True)