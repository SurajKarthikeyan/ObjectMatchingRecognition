import torch
import math
from models.LightGlueMaster.lightglue.utils import load_image, rbd
from config import *
import cv2
from PIL import Image
import numpy as np
"""
Matches the partial image to the whole
"""

def distance(point1, point2):
    return torch.norm(point2 - point1)

def group_points(points, threshold):
    groups = []
    num_points = points.size(0)
    visited = set()

    for i in range(num_points):
        if i not in visited:
            current_group = []
            current_group.append(i)
            visited.add(i)

            for j in range(i + 1, num_points):
                if j not in visited:
                    if distance(points[i], points[j]) <= threshold:
                        current_group.append(j)
                        visited.add(j)
            groups.append(current_group)

    return groups

def calculate_center_radius(points, group):
    '''
    This function take list of points and calculate center and radius of that points group
    '''
    furthest_point = [0, 0]
    group_points = points[group]
    center = torch.mean(group_points, dim=0).cpu().numpy()
    center = tuple(int(coord) for coord in center)
    # Find the furthest point from the center in the points group
    for idx in group:
        point = points[idx].cpu().numpy()
        dist_x = abs(abs(point[0]) - abs(center[0]))
        dist_y = abs(abs(point[1]) - abs(center[1]))
        if dist_x > furthest_point[0]: furthest_point[0] = point[0]
        if dist_y > furthest_point[1]: furthest_point[1] = point[1]

    # calculate the radius sqrt((x2-x1) ^2 + (y2-y1) ^2)
    radius = math.sqrt((furthest_point[0] - center[0])**2 + (furthest_point[1] - center[1])**2)
    return center, int(radius)

def draw_transparent_circles_on_image(image: Image, circles: list) -> Image:
    # Convert PIL image to OpenCV format
    image_cv = np.array(image)
    image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGB2BGR)

    # Draw transparent circles on the image
    for circle in circles:
        circle_center, circle_radius = circle
        overlay = image_cv.copy()
        cv2.circle(overlay, circle_center, circle_radius, (0, 0, 255), -1)  # Red circle (BGR format)
        alpha = 0.5  # Change the transparency level if needed
        cv2.addWeighted(overlay, alpha, image_cv, 1 - alpha, 0, image_cv)

    # Convert OpenCV format back to PIL
    image_pil = Image.fromarray(cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB))
    return image_pil

def add_matching(part_path, whole_path, name="test"):
    partial_image = load_image(part_path)
    whole_image = load_image(whole_path)

    feats0 = extractor.extract(partial_image.to(device))
    feats1 = extractor.extract(whole_image.to(device))
    matches01 = matcher({"image0": feats0, "image1": feats1})
    feats0, feats1, matches01 = [
        rbd(x) for x in [feats0, feats1, matches01]
    ]  # remove batch dimension

    kpts0, kpts1, matches = feats0["keypoints"], feats1["keypoints"], matches01["matches"]
    m_kpts0, m_kpts1 = kpts0[matches[..., 0]], kpts1[matches[..., 1]]  # tensors array
    print("Finished keypoint matching")

    # lets get jiggy with it
    # Set a threshold distance for grouping points
    threshold_distance = 1000.0  # You can adjust this threshold
    threshold_group_size = 3

    resultL = group_points(m_kpts0, threshold_distance)
    #print(resultL)
    resultL = [group for group in resultL if len(group) >= threshold_group_size]
    circles_listL = []
    # print("Groups of points that are close to each other in left image:")
    for group in resultL:
        result_tup = calculate_center_radius(m_kpts0, group)
        circles_listL.append(result_tup)

    resultR = group_points(m_kpts1, threshold_distance)
    #print(resultR)
    resultR = [group for group in resultR if len(group) >= threshold_group_size]
    circles_listR = []
    # print("Groups of points that are close to each other in right image:")
    for group in resultR:
        result_tup = calculate_center_radius(m_kpts1, group)
        circles_listR.append(result_tup)

    # Draw circles
    image_with_circlesL = draw_transparent_circles_on_image(Image.open(part_path), circles_listL)
    image_with_circlesR = draw_transparent_circles_on_image(Image.open(whole_path), circles_listR)

    image_with_circlesL.save(path_control + "MatchMakingOutput/" + "LeftImage" + ".png")
    image_with_circlesR.save(path_control + "MatchMakingOutput/" + "RightImage" + ".png")

    print("Finished saving image")

"""
Creates the final image to display
"""

def create_final_image():
    pass
