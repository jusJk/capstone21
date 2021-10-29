# File for backeend functions to do post processing on
from PIL import ImageDraw, Image
import cv2 as cv
import numpy as np
import pandas as pd
import os
import math
from datetime import datetime
import itertools


def render_image(frame, bboxes, output_image_file, outline_color='yellow', linewidth=10):
    """Render images with overlain outputs."""
    image = Image.open(frame)
    draw = ImageDraw.Draw(image)
    for bbox_info in bboxes:
        box = [value for key, value in bbox_info.items() if 'bbox' in key.lower()][0]
        if (box[2] - box[0]) >= 0 and (box[3] - box[1]) >= 0:
            draw.rectangle(box, outline=outline_color)
            for i in range(linewidth):
                x1 = max(0, box[0] - i)
                y1 = max(0, box[1] - i)
                x2 = min(image.size[0], box[2] + i)
                y2 = min(image.size[1], box[3] + i)
                draw.rectangle(box, outline=outline_color)
    image.save(output_image_file)


def crop_image(frame, box, output_cropped_file):
    """Create crop image """
    image = Image.open(frame)
    if (box[2] - box[0]) >= 0 and (box[3] - box[1]) >= 0:
        image = image.crop((box[0],box[1],box[2],box[3]))
    image.save(output_cropped_file,"JPEG")

def save_image(frame, output):
    image = Image.open(frame)
    image.save(output,"JPEG")

def create_directories(model, id):

    curr_time = datetime.now().strftime("%d%m%y_%H%M%S")

    # Create directories for input and output images
    if not os.path.isdir(f"./models/{model}/input"):
        os.mkdir(f"./models/{model}/input")
        os.mkdir(f"./models/{model}/output")

    if not os.path.isdir(f"./models/{model}/input/{id}"):
        os.mkdir(f"./models/{model}/input/{id}")
        os.mkdir(f"./models/{model}/output/{id}")

    if not os.path.isdir(f"./models/{model}/input/{id}/{curr_time}"):
        os.mkdir(f"./models/{model}/input/{id}/{curr_time}")
        os.mkdir(f"./models/{model}/output/{id}/{curr_time}")

    return f"./models/{model}/input/{id}/{curr_time}", f"./models/{model}/output/{id}/{curr_time}"

def plot_keypoints(results, image_filename, image_path, output_path, render_limbs=True):
    """Renders keypoints on input image

    Args:
        results (dict): Inference output from BodyPoseNet prediction
        image_filename ([type]): File name of image used during inference
        image_path (str): Path to input image
        render_limbs (bool): If true, render limb connections

    Returns:
        (numpy.ndarray): Image with keypoints and limb connections rendered
    """

    image_res = results['results'][image_filename]
    skeleton_edge_names = results['skeleton_edge_names']
    colors = [[255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0], [170, 255, 0], [85, 255, 0], [0, 255, 0],
              [0, 255, 85], [0, 255, 170], [0, 255, 255], [
                  0, 170, 255], [0, 85, 255], [0, 0, 255], [85, 0, 255],
              [170, 0, 255], [255, 0, 255], [255, 0, 170], [255, 0, 85], [0, 85, 85]]

    stickwidth = 1  # width of limb connections
    radius = 2  # radius of keypoint circles
    canvas = cv.imread(image_path)
    to_plot = cv.imread(image_path)
    for person in image_res:
        total = person['total']
        person = list(person.items())
        for i in range(total-2):  # exclude last 2 elements which are score and total keypoints
            center = person[i][1]
            cv.circle(canvas, (int(center[0]), int(
                center[1])), radius, colors[i], thickness=-1)
    to_plot = cv.addWeighted(to_plot, 0.3, canvas, 0.7, 0)

    if not render_limbs:
        cv.imwrite(output_path,to_plot)

    for person in image_res:
        # Each edge is a joint represented by tuple (keypoint_a, keypoint_b)
        for i, edge in enumerate(skeleton_edge_names):
            keypoint_a = edge[0]
            keypoint_b = edge[1]
            if keypoint_a in person and keypoint_b in person:  # If both keypoints were identified
                # Get the x coords of each keypoint
                X = (person[keypoint_a ][1], person[keypoint_b][1])
                # Get the y coords of each keypoint
                Y = (person[keypoint_a ][0], person[keypoint_b][0])
                cur_canvas = canvas.copy()
                mX = np.mean(X)
                mY = np.mean(Y)
                length = ((X[0] - X[1]) ** 2 + (Y[0] - Y[1]) ** 2) ** 0.5
                angle = math.degrees(math.atan2(X[0] - X[1], Y[0] - Y[1]))
                polygon = cv.ellipse2Poly((int(mY), int(mX)), (int(
                    length/2), stickwidth), int(angle), 0, 360, 1)
                cv.fillConvexPoly(cur_canvas, polygon, colors[i])
                canvas = cv.addWeighted(canvas, 0.4, cur_canvas, 0.6, 0)
    cv.imwrite(output_path, canvas)


def replace_in_markdown(mapping, md_path):
    with open(md_path, 'r') as md:
        text = md.readlines()
        lines = []
        for line in text:
            lines.append(line)
            for key in mapping.keys():
                if key in line:
                    lines[-1] = line.replace(key, mapping[key])

        new_text = "\n".join(lines)
    return new_text

def check_request(request):
    # Load input images
    files = request.files.to_dict(flat=False)['image']

    # Load filenames
    filenames = request.form.getlist('filename')

    if len(files)==0:
        return {'error':'Image not found'}

    if len(filenames)==0:
        return {'error':'No filename for image'}

    if len(files) != len(filenames):
        return {'error':'Number of images and filenames do not match'}

    else:
        return True

# [x1, y1, x2, y2] and [x1, y1, x2, y2] 
def calculate_iou_from_coords(bx1, bx2):
    #map list of coordinates into bounding box
    bb1, bb2 = {},{}
    bb1['x1'], bb1['y1'], bb1['x2'], bb1['y2'] = bx1
    bb2['x1'], bb2['y1'], bb2['x2'], bb2['y2'] = bx2

    # determine the coordinates of the intersection rectangle
    x_left = max(bb1['x1'], bb2['x1'])
    y_top = max(bb1['y1'], bb2['y1'])
    x_right = min(bb1['x2'], bb2['x2'])
    y_bottom = min(bb1['y2'], bb2['y2'])
    
    # compute the area of both AABBs
    bb1_area = (bb1['x2'] - bb1['x1']) * (bb1['y2'] - bb1['y1'])
    bb2_area = (bb2['x2'] - bb2['x1']) * (bb2['y2'] - bb2['y1'])
    if x_right < x_left or y_bottom < y_top:
        return 0.0, bb1_area, bb2_area

    # The intersection of two axis-aligned bounding boxes is always an
    # axis-aligned bounding box
    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = intersection_area / float(bb1_area + bb2_area - intersection_area)

    return iou, bb1_area, bb2_area

def filter_overlapping_bbox(lpd_response):

    for i, info in enumerate(lpd_response):
        bboxes = lpd_response[i]['all_bboxes']
        bboxes_idx = range(len(bboxes))
        to_remove_set = set() #Ensure we only remove the necessary image once
        for combinations in itertools.combinations(bboxes_idx, 2):
            first, second = combinations
            (iou, first_area, second_area) = calculate_iou_from_coords(bboxes[first]['bbox'], bboxes[second]['bbox'])
            if iou > 0.1:
                if first_area < second_area:
                    to_remove_set.add(first)
                else:
                    to_remove_set.add(second)
        
        to_remove_ls = list(to_remove_set)
        to_remove_ls.sort(reverse = True) #Sorting in reverse to remove index from the back (prevent index out of bounds due to removal)
        for to_remove in to_remove_ls:
            lpd_response[i]['all_bboxes'].pop(to_remove)
    
    return lpd_response