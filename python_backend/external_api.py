from app import app
from flask import request, send_file
from flask_cors import CORS, cross_origin
from utils.utils import crop_image, render_image, create_directories, plot_keypoints, save_image, chop_image, draw_confidence_heat_map, replace_in_markdown
import pandas as pd

import json
import os
from datetime import datetime
CORS(app)

import sys
sys.path.insert(1, '/app/triton_client/')

# from models.lpdnet.lpd_model_class import LpdModelClass
# from models.lprnet.lpr_model_class import LprModelClass
# from models.bpnet.bodyposenet_model_class import BodyPoseNetClass


BASE_URL = 'http://localhost:5000/'


@app.route('/api/lpdlprnet/<id>',methods= ['POST', 'GET'])
def call_combined(id):

    """
    This function responds to the external API call of obtaining
    lpd and then lpr.

    :return: JSON object 
    """
    
    lpr = LprModelClass(id)
    lpd = LpdModelClass(id)

    if request.method=='GET':

        return lpr.status()
    
    elif request.method=='POST':

        # Create directories for input and output images
        now = datetime.now()
        curr_time = now.strftime("%H%M%S")
        create_directories('lpdnet',id, curr_time)
        create_directories('lprnet',id, curr_time)

        # Load input images
        files = request.files.to_dict(flat=False)['image']

        # Load filenames
        filenames = request.form.getlist('filename')
        
        images = {}
        # Save input images
        for i, f in enumerate(files):
            images[filenames[i]] = f
            f.save(f"triton_client/lpdnet/input/{id}/{curr_time}/{filenames[i]}")
        
        # Call triton inference server
        lpd_response = lpd.predict(f"triton_client/lpdnet/input/{id}/{curr_time}")

        # Save the lpd output images into a new folder
        processed = {}
        reverse_mapping = {}
        for i, info in enumerate(lpd_response):
            if info['HTTPStatus']==204:
                # No inference bounding box was found
                processed[i] = info
            else:
                # info is a list of bbox, bbox is a dict containing a list (bbox)
                # and a single number, confidence score
                for j, bbox_info in enumerate(info["all_bboxes"]):
                    crop_image(images[info['file_name']],bbox_info['bbox'],f"triton_client/lpdnet/output/{id}/{curr_time}/{j}_{info['file_name']}")
                    crop_image(images[info['file_name']],bbox_info['bbox'],f"triton_client/lprnet/input/{id}/{curr_time}/{j}_{info['file_name']}")
                    
                    reverse_mapping[f"{j}_{info['file_name']}"] = i
                    
                    bbox_info[f"{j}_bbox"] = bbox_info.pop('bbox')
                
                if id=='internal':
                    render_image(images[info['file_name']],info["all_bboxes"],f"triton_client/lpdnet/output/{id}/{curr_time}/overlay_lpdnet_{info['file_name']}")
                    info['overlay_image'] = f"triton_client/lpdnet/output/{id}/{curr_time}/overlay_lpdnet_{info['file_name']}"

                processed[i] = info

        # Call LPR on output of LPD
        lpr_response = lpr.predict(f"triton_client/lprnet/input/{id}/{curr_time}")

        # Process response to return
        for lpr_info in lpr_response:
            file_name = lpr_info['file_name']
            index = file_name.split("_")[0]
            temp = {}
            temp['license_plate'] = lpr_info['license_plate']
            temp['confidence_scores'] = lpr_info['confidence_scores']
            processed[reverse_mapping[file_name]][f"{index}_lpr"] = temp

        return processed        
    
    else:
        return {'code':404,'error':'Request not found'}


# REFACTOR THIS PLEASE
def evaluate_lpd(image_path, filename, id, save_as,n):
    import cv2

    lpd = LpdModelClass(id)
    now = datetime.now()
    curr_time = now.strftime("%d%m%y_%H%M%S")
    create_directories('lpdnet',id, curr_time)

    subimages = chop_image(image_path,  n)

    # Save input images
    for i, f in enumerate(subimages):
        cv2.imwrite(f"triton_client/lpdnet/input/{id}/{curr_time}/{str(i) + filename.split('.')[0] + '.png'}", f)
        
    lpd_response = lpd.predict(f"triton_client/lpdnet/input/{id}/{curr_time}")
    draw_confidence_heat_map(lpd_response, image_path, save_as, n)

    # delete subimages
    for i, f in enumerate(subimages):
        os.remove(f"triton_client/lpdnet/input/{id}/{curr_time}/{str(i) + filename.split('.')[0] + '.png'}")


@app.route('/api/lpdlprnet/explain/<id>',methods= ['POST', 'GET'])
def call_explain_combined(id):
    """
    This is a function to orchestrate the following steps: 
    1. run lpd-lpr pipeline and spit out predictions
    2. run evaluation of lpd and save overlay/results
    3. replace placeholders in markdown file with their respective dynamic values
    
    """
    #level of detail:
    n = 11

    lpr = LprModelClass(id)
    lpd = LpdModelClass(id)

    # Create directories for input and output images
    now = datetime.now()
    curr_time = now.strftime("%H%M%S")
    create_directories('lpdnet',id, curr_time)
    create_directories('lprnet',id, curr_time)

    # Load input images
    files = request.files.to_dict(flat=False)['image']

    # Load filenames
    filenames = request.form.getlist('filename')

    #STATIC FILENAMES
    save_as = f"triton_client/lpdnet/output/{id}/{curr_time}/heatmap_{filenames[0]}"
    baseimage = f"triton_client/lpdnet/input/{id}/{curr_time}/{filenames[0]}"
    
    images = {}

    # Save input images --> for explain, only use 1st file
    images[filenames[0]] = files[0]
    files[0].save(baseimage)

    # SEND TO LPD
    lpd_response = lpd.predict(f"triton_client/lpdnet/input/{id}/{curr_time}")

    processed = {}
    reverse_mapping = {}
    i, info = 0, lpd_response[0]

    # DYNAMIC FILENAMES
    lpdout = f"triton_client/lpdnet/output/{id}/{curr_time}/exp_{info['file_name']}"
    lprin = f"triton_client/lprnet/input/{id}/{curr_time}/exp_{info['file_name']}"
    lprin_folder = f"triton_client/lprnet/input/{id}/{curr_time}"
    demopic = f"triton_client/lpdnet/output/{id}/{curr_time}/overlay_lpdnet_{info['file_name']}"

    if info['HTTPStatus']==204:
        # No inference bounding box was found
        processed[i] = info
        save_image(images[info['file_name']], lprin)
        reverse_mapping[f"exp_{info['file_name']}"] = i

    else:
        # info is a list of bbox, bbox is a dict containing a list (bbox)
        # and a single number, confidence score
        for j, bbox_info in enumerate(info["all_bboxes"]):
            crop_image(images[info['file_name']],bbox_info['bbox'],lpdout)
            crop_image(images[info['file_name']],bbox_info['bbox'],lprin)
            reverse_mapping[f"exp_{info['file_name']}"] = i
            bbox_info[f"exp_bbox"] = bbox_info.pop('bbox')
            
        if id=='internal': 
            
            render_image(images[info['file_name']],info['all_bboxes'], demopic)
            info['overlay_image'] = demopic    

    processed[i] = info
    evaluate_lpd(baseimage, filenames[0], id, save_as, n)

     # Call LPR on output of LPD
    lpr_response = lpr.predict(lprin_folder)
    
    # Process response to return
    for lpr_info in lpr_response:
        file_name = lpr_info['file_name']
        index = file_name.split("_")[0]
        temp = {}
        temp['license_plate'] = list(lpr_info['license_plate'])
        temp['confidence_scores'] = lpr_info['confidence_scores']
        processed[reverse_mapping[file_name]][f"exp_lpr"] = temp
     
        
    # replace markdown placeholders with custom images
    image_replace = {
        '%placeholder1%' : f"{baseimage}", 
        '%placeholder2%' : f"{demopic}",
        '%placeholder3%' : f"{lpdout}",
        '%placeholder4%' : f"{save_as}",
        '%placeholder5%' : pd.DataFrame(info['all_bboxes']).to_html(),
        '%placeholder6%' : pd.DataFrame(temp).assign(lp = '')[['lp', 'license_plate', 'confidence_scores']].rename(columns={'lp':lpr_info['license_plate']}).to_html(index=False, ),
    }
    
    
    return {'explain_markdown': replace_in_markdown(image_replace, "database/lpdlprnet/lpdlprnet_explainability_dynamic.md")}


