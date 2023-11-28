import Cropper from 'cropperjs';
const image = document.getElementsByClassName('croppingimage');
const cropper = new Cropper(image, {
  aspectRatio: 0,
});