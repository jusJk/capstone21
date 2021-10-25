from app import app
from flask import request, send_file, make_response
from flask_cors import CORS, cross_origin
from utils.utils import crop_image, render_image, create_directories, save_image, check_request, calculate_iou_from_coords
import itertools
import cv2

import json
import os
CORS(app)

from .lpd_model_class import LpdModelClass

@app.route('/api/lpdnet/<id>',methods= ['POST', 'GET'])
def call_lpdnet(id):

    """
    This function responds to the external API call of obtaining
    lpdnet

    :return: JSON object
    """
    mapping = json.load(open('/app/models/lpdnet/database/mapping.json'))
    LOGGING = True #Saves output images into the folders
    THRESHOLD = 0.9 #Threshold for bbox to be tuned

    if id not in mapping: return make_response({'error':"Bad Request - Invalid ID"},400)

    model_name=mapping[id]

    try:
        lpd = LpdModelClass(id,model_name)
    except ValueError:
        return make_response({'error':"Model not found on triton server"},503)

    if request.method=='GET':
        status = lpd.status()
        if status['status']=='Active':
            return make_response(status,200)
        return make_response(status,503)

    elif request.method=='POST':

        # Load input images
        files = request.files.to_dict(flat=False)['image']

        # Load filenames
        filenames = request.form.getlist('filename')

        output = check_request(request)

        if output!=True: return make_response(output,400)

        # Create directories for input and output images
        input_path, output_path = create_directories('lpdnet',id)

        images = {}
        # Save input images
        for i, f in enumerate(files):
            images[filenames[i]] = f
            f.save(f"{input_path}/{filenames[i]}")

        # Call triton inference server
        try:
            response = lpd.predict(input_path)
        except FileNotFoundError:
            return make_response({'error':"Internal Server Error"},503)
            
        # Calculate IOU from among all permutations of bboxes for each image response and remove smaller box if iou > 0.1
        for i, info in enumerate(response):
            bboxes = response[i]['all_bboxes']
            bboxes_idx = range(len(bboxes))
            to_remove_set = set() #Ensure we only remove the necessary image once
            for combinations in itertools.combinations(bboxes_idx, 2): #Comparing between all combinations of bboxes
                first, second = combinations
                (iou, first_area, second_area) = calculate_iou_from_coords(bboxes[first]['bbox'], bboxes[second]['bbox'])
                if iou > 0:
                    if first_area < second_area:
                        to_remove_set.add(first)
                    else:
                        to_remove_set.add(second)
            
            to_remove_ls = list(to_remove_set)
            to_remove_ls.sort(reverse = True) #Sorting in reverse to remove index from the back (prevent index out of bounds due to removal)
            for to_remove in to_remove_ls:
                response[i]['all_bboxes'].pop(to_remove)

        # Process response to return
        processed = {}
        for i, info in enumerate(response):
            if info['HTTPStatus']==204:
                # No inference bounding box was found

                del info['HTTPStatus']

                processed[i] = info
            else:
                # info is a list of bbox, bbox is a dict containing a list (bbox)
                # and a single number, confidence score
                for j, bbox_info in enumerate(info["all_bboxes"]):

                    if LOGGING: crop_image(images[info['file_name']],bbox_info['bbox'],f"{output_path}/{j}_{info['file_name']}")

                    confidence_score=bbox_info['confidence_score']
                    if confidence_score < THRESHOLD:
                        continue

                if id=='internal':
                    render_image(images[info['file_name']],info["all_bboxes"],f"{output_path}/overlay_lpdnet_{info['file_name']}")
                    info['overlay_image'] = f"{output_path}/overlay_lpdnet_{info['file_name']}"

                del info['HTTPStatus']

                processed[i] = info

        return make_response(processed,200)
#
# def evaluate_lpd(image_path, filename, id, save_as,n):
#
#     mapping = json.load(open('/app/models/lpdnet/database/mapping.json'))
#     LOGGING = True #Saves output images into the folders
#     THRESHOLD = 0.9 #Threshold for bbox to be tuned
#
#     if id not in mapping: return make_response({'error':"Bad Request - Invalid ID"},400)
#
#     model_name=mapping[id]
# 
#     try:
#         lpd = LpdModelClass(id,model_name)
#     except ValueError:
#         return make_response({'error':"Model not found on triton server"},503)
#
#     # Create directories for input and output images
#     input_path, output_path = create_directories('lpdnet',id)
#
#     subimages = chop_image(image_path,  n)
#
#     # Save input images
#     for i, f in enumerate(subimages):
#         cv2.imwrite(f"{input_path}/{str(i) + filename.split('.')[0] + '.png'}", f)
#
#     response = lpd.predict(input_path)
#
#     draw_confidence_heat_map(response, image_path, save_as, n)
#
#     # delete subimages
#     for i, f in enumerate(subimages):
#         os.remove(f"{input_path}/{str(i) + filename.split('.')[0] + '.png'}")
