import torch
from PIL import Image
from models.LightGlueMaster.lightglue import LightGlue, SuperPoint
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # 'mps', 'cpu'

extractor = SuperPoint(max_num_keypoints=2048).eval().to(device)  # load the extractor
matcher = LightGlue(features="superpoint").eval().to(device)

path_control = 'static/' #'webapp/static/'
path_web = '' #'webapp/'

def scale_image(img, max_width, max_height):
    # Get the original width and height
    width, height = img.size

    # Calculate the aspect ratio
    aspect_ratio = width / height

    # Calculate new dimensions to fit within the specified parameters
    new_width = min(width, max_width)
    new_height = int(new_width / aspect_ratio)

    # Check if the new height exceeds the maximum height
    if new_height > max_height:
        new_height = max_height
        new_width = int(new_height * aspect_ratio)

    # Resize the image
    resized_img = img.resize((new_width, new_height))
    return resized_img