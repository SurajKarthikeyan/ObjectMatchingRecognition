# ObjectMatchingRecognition

## Prerequistes
1. Download Node.js in conda environment with this command:
```bash
conda install -c conda-forge nodejs
```
2. Check node and npm versions to make sure you have Node.js installed:
```bash
node -v
npm -v
```
3. Download Cropper.js:
```bash
npm install cropperjs
```
4. Download the pretrained BASNet model from this [link](https://drive.google.com/file/d/1s52ek_4YTDRt_EOkx1FS53u-vJa0c4nu/view) and put it in webapp/models/BASNetMaster/saved_models/basnet_bsi

## Start the website
1. After you installed Cropper.js, please move the "cropperjs" folder (not the one in node_modules) to static folder
2. Go to webapp/start.py and run the Python file
2. Click the localhost link
3. Choose your image that you want to compare the cropped image too
4. Crop the image from your webcam and click generate to view result
