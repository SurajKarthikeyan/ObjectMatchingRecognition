"""
BASnet file derived from basnet_demo.ipynb

"""
from PIL import Image
# from IPython.display import display
import os
from skimage import io, transform
import torch
import torchvision
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms  # , utils

import numpy as np

from models.master.model import BASNet
from models.master.data_loader import SalObjDataset
from models.master.data_loader import ToTensorLab
from models.master.data_loader import RescaleT

prediction_dir = 'static/BASNetMade/'


def normPRED(d):
    ma = torch.max(d)
    mi = torch.min(d)

    dn = (d - mi) / (ma - mi)

    return dn


def save_output(image_name, pred, d_dir):
    predict = pred
    predict = predict.squeeze()
    predict_np = predict.cpu().data.numpy()

    im = Image.fromarray(predict_np * 255).convert('RGB')
    img_name = image_name.split("/")[-1]
    image = io.imread(image_name)
    imo = im.resize((image.shape[1], image.shape[0]), resample=Image.BILINEAR)

    pb_np = np.array(imo)

    aaa = img_name.split(".")
    bbb = aaa[0:-1]
    imidx = bbb[0]
    for i in range(1, len(bbb)):
        imidx = imidx + "." + bbb[i]

    imo.save(d_dir + imidx + '.png')


def data_handle(to_bas):
    image_list = ['static/uploads/' + to_bas]

    # 1. dataload
    test_salobj_dataset = SalObjDataset(img_name_list=image_list, lbl_name_list=[],
                                        transform=transforms.Compose([RescaleT(256), ToTensorLab(flag=0)]))
    test_salobj_dataloader = DataLoader(test_salobj_dataset, batch_size=1, shuffle=False, num_workers=1)

    # 2. load BASNet
    net = bas_start()

    # --------- 3. inference for each image ---------
    for i_test, data_test in enumerate(test_salobj_dataloader):

        print("inferencing:", image_list[i_test].split("/")[-1])

        inputs_test = data_test['image']
        inputs_test = inputs_test.type(torch.FloatTensor)

        if torch.cuda.is_available():
            inputs_test = Variable(inputs_test.cuda())
        else:
            inputs_test = Variable(inputs_test)

        d1, d2, d3, d4, d5, d6, d7, d8 = net(inputs_test)

        # normalization
        pred = d1[:, 0, :, :]
        pred = normPRED(pred)

        # save results to test_results folder
        save_output(image_list[i_test], pred, prediction_dir)

        del d1, d2, d3, d4, d5, d6, d7, d8

    # 4. Mask Image
    img_input = Image.open('static/uploads/' + to_bas)

    empty = Image.new("RGBA", img_input.size, 0)
    mask = Image.open('static/BASNetMade/' + to_bas).convert("L")
    ref = Image.open('static/uploads/' + to_bas)
    img = Image.composite(ref, empty, mask)

    img.save('static/BASNetMask/' + to_bas)

    return 'static/BASNetMask/' + to_bas


"""
Runs on website open
Gets the pretrained weights
"""


def bas_start():
    model_dir = 'models/master/saved_models/basnet_bsi/basnet.pth'  # pretrained model
    print("...load BASNet...")
    net = BASNet(3, 1)
    net.load_state_dict(torch.load(model_dir))
    if torch.cuda.is_available():
        net.cuda()
    net.eval()
    print("...BASNet Loaded...")
    return net


"""
removes the background of the partial image
"""


def remove_background():
    pass


"""
Matches the partial image to the whole
"""


def add_matching():
    pass


"""
Creates the final image to display
"""


def create_final_image():
    pass
