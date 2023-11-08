from models.LightGlueMaster.lightglue.utils import load_image, rbd
from config import *
from models.LightGlueMaster.lightglue import viz2d

"""
Matches the partial image to the whole
"""

def add_matching(part_path, whole_path, name="test"):
    print(part_path) #partial image path
    print(whole_path) #image to compare against

    partial_image = load_image(part_path)
    whole_image = load_image(whole_path)

    feats0 = extractor.extract(partial_image.to(device))
    feats1 = extractor.extract(whole_image.to(device))
    matches01 = matcher({"image0": feats0, "image1": feats1})
    feats0, feats1, matches01 = [
        rbd(x) for x in [feats0, feats1, matches01]
    ]  # remove batch dimension

    kpts0, kpts1, matches = feats0["keypoints"], feats1["keypoints"], matches01["matches"]
    m_kpts0, m_kpts1 = kpts0[matches[..., 0]], kpts1[matches[..., 1]]
    print("Finished keypoint matching")
    #axes = viz2d.plot_images([partial_image, whole_image])
    #viz2d.plot_matches(m_kpts0, m_kpts1, color="lime", lw=0.2, name="test")


"""
Creates the final image to display
"""


def create_final_image():
    pass