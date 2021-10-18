# File for backeend functions to do post processing on
from PIL import ImageDraw, Image
import cv2 as cv
import numpy as np
import os
import math
from datetime import datetime


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


def chop_image(im_path, n): 
    """
    Chop image into n segments
    """
    org = cv.imread(im_path)
   
    im = org.copy()
    M = im.shape[0]//n
    N = im.shape[1]//n
    tile_coord = [[x,x+M,y,y+N] for x in range(0,im.shape[0],M) for y in range(0,im.shape[1],N)]
    response =[]
    for i,matrix in enumerate(tile_coord):
        a,b,c,d = matrix
        ts = im.copy()
        ts[a:b, c:d] = 0
        response.append(ts)
    return response
    
def map_confidence_to_chunk(responses, filename):
    conf = {}
    for r in responses:
        key = r['file_name'].replace(filename,'')
        try:
            sc = r['all_bboxes'][0]['confidence_score']
        except:
            sc = 0.01
        conf[key] = sc
    
    return conf

def color_chunks(original_image_path, conf, save_as, n=2):
    import matplotlib.pyplot as plt
    org = cv.imread(original_image_path)
    org = cv.cvtColor(org, cv.COLOR_BGR2RGB)
    im = org.copy()
    M = im.shape[0]//n
    N = im.shape[1]//n
    tile_coord = [[x,x+M,y,y+N] for x in range(0,im.shape[0],M) for y in range(0,im.shape[1],N)]
    response =[]
    coef = get_coefficients(conf)
    mean = sum(coef)/len(coef)
    for i,matrix in enumerate(tile_coord):
        a,b,c,d = matrix
        color(im[a:b,c:d], i, coef, mean )
        
    plt.imshow(org)
    plt.imshow(im, alpha=0.6)
    plt.savefig(save_as)
        
def conf_color(x, max_v): 
    return (max_v-x)*255/max_v     

def draw_confidence_heat_map(responses, filename, save_as, n): 
    enforce_png_name = filename.split('/')[-1].split('.')[0] + '.png'
    print(responses, flush=True)
    conf = map_confidence_to_chunk(responses,enforce_png_name) 
    color_chunks(filename, conf, save_as, n)
    

def get_coefficients(conf):
    import pandas as pd
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.linear_model import LinearRegression
    enc = OneHotEncoder()
    df = pd.DataFrame([int(k) for k,v in conf.items()])
    y = [v for v in conf.values()]
    X = 1-enc.fit_transform(df).toarray()
    reg = LinearRegression().fit(X, y)
    
    return reg.coef_

def color(matrix, i, coefs, mean):
    coef=coefs[i]
    for chunk in matrix: 
        for pixel in chunk:
            pixel[0] = 0
            pixel[1] = 0
            pixel[2] = 0
            c, s = reg_color(coef, mean)
            pixel[c] = s 
         

def reg_color(coef, mean):
    if coef >= 0 :
        #red means coefficient is positive. adding it increases conf
        return 0, abs(coef-mean)*255/mean
    if coef < 0:
        #blue means coefficient is negative, adding it reduces conf
        return 2, abs(coef-mean)*255/mean


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