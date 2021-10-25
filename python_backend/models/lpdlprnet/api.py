from app import app
from flask import request, send_file, make_response
from flask_cors import CORS, cross_origin
from utils.utils import create_directories, check_request, crop_image, render_image, replace_in_markdown, save_image
from models.lpdlprnet.lpdlprutils import chop_image, draw_confidence_heat_map
import pandas as pd
import datetime

import json
import os
CORS(app)

from models.lpdnet.lpd_model_class import LpdModelClass
from models.lprnet.lpr_model_class import LprModelClass


@app.route('/api/lpdlprnet/<id>',methods= ['POST', 'GET'])
def call_combined(id):

    """
    This function responds to the external API call of obtaining
    lpd and then lpr.

    :return: JSON object
    """

    lpd_mapping = json.load(open('/app/models/lpdlprnet/database/lpd_mapping.json'))
    lpr_mapping = json.load(open('/app/models/lpdlprnet/database/lpr_mapping.json'))
    LOGGING = True #Saves output images into the folders
    LPD_THRESHOLD = 0.6 #Threshold to filter images
    LPR_THRESHOLD = 0.6

    if (id not in lpd_mapping) or (id not in lpr_mapping):
        return make_response({'error':"Bad Request - Invalid ID"},400)

    try:
        lpr = LprModelClass(id, lpr_mapping[id])
        lpd = LpdModelClass(id, lpd_mapping[id])
    except ValueError:
        return make_response({'error':"Model not found on triton server"},503)

    if request.method=='GET':

        lpd_status = lpd.status()
        lpr_status = lpr.status()

        if lpd_status['status']=='Active' and lpr_status['status']=='Active':
            return make_response(lpd_status,200)
        return make_response(lpd_status,503)

    elif request.method=='POST':

        # Load input images
        files = request.files.to_dict(flat=False)['image']

        # Load filenames
        filenames = request.form.getlist('filename')

        output = check_request(request)

        if output!=True: return make_response(output,400)

        # Create directories for input and output images
        input_path, output_path = create_directories('lpdlprnet',id)

        images = {}
        # Save input images
        for i, f in enumerate(files):
            images[filenames[i]] = f
            f.save(f"{input_path}/{filenames[i]}")

        # Call triton inference server
        try:
            lpd_response = lpd.predict(input_path)
        except FileNotFoundError:
            return make_response({'error':"Internal Server Error"},503)

        # Save the lpd output images into a new folder
        processed = {}
        reverse_mapping = {}
        for i, info in enumerate(lpd_response):
            if info['HTTPStatus']==204:
                # No inference bounding box was found

                del info['HTTPStatus']

                processed[i] = info
            else:
                # info is a list of bbox, bbox is a dict containing a list (bbox)
                # and a single number, confidence score
                for j, bbox_info in enumerate(info["all_bboxes"]):
                    confidence_score=bbox_info['confidence_score']
                    if confidence_score < LPD_THRESHOLD:
                        continue
                    crop_image(images[info['file_name']],bbox_info['bbox'],f"{output_path}/{j}_{info['file_name']}")

                    reverse_mapping[f"{j}_{info['file_name']}"] = i

                    bbox_info[f"{j}_bbox"] = bbox_info.pop('bbox')

                del info['HTTPStatus']

                processed[i] = info

        # Call triton inference server
        try:
            lpr_response = lpr.predict(output_path)
        except FileNotFoundError:
            return make_response({'error':"Internal Server Error"},503)

        # Process response to return
        for lpr_info in lpr_response:

            temp = {}

            confidence_scores = lpr_info['confidence_scores'] #List of confidence scores
            license_plate = lpr_info['license_plate']

            new_lp = [char for i, char in enumerate(license_plate) if confidence_scores[i]> LPR_THRESHOLD]
            new_cs = [c for c in confidence_scores if c > LPR_THRESHOLD]

            file_name = lpr_info['file_name']
            index = file_name.split("_")[0]

            # No license plate was detected -- filter it out
            if len(new_lp)==0:
                del processed[reverse_mapping[file_name]]["all_bboxes"][index]

            temp['license_plate'] = ''.join(new_lp)
            temp['confidence_scores'] = new_cs

            processed[reverse_mapping[file_name]][f"{index}_lpr"] = temp

        # Overlay images in the end to avoid errors
        if id=='internal':
            for i, info in enumerate(lpd_response):
                if len(info["all_bboxes"])!=0:
                    render_image(images[info['file_name']],info["all_bboxes"],f"{output_path}/overlay_lpdnet_{info['file_name']}")
                    processed[i]['overlay_image'] = f"{output_path}/overlay_lpdnet_{info['file_name']}"


        return make_response(processed,200)


@app.route('/api/lpdlprnet/explain/<id>',methods= ['POST', 'GET'])
def call_explain_combined(id):
    """
    This is a function to orchestrate the following steps:
    1. run lpd-lpr pipeline and spit out predictions
    2. run evaluation of lpd and save overlay/results
    3. replace placeholders in markdown file with their respective dynamic values

    """
    #level of detail:
    n =85

    lpd_mapping = json.load(open('/app/models/lpdlprnet/database/lpd_mapping.json'))
    lpr_mapping = json.load(open('/app/models/lpdlprnet/database/lpr_mapping.json'))
    LOGGING = True #Saves output images into the folders
    LPD_THRESHOLD = 0.6 #Threshold to filter images
    LPR_THRESHOLD = 0.6

    if (id not in lpd_mapping) or (id not in lpr_mapping) or (id!='internal'):
        return make_response({'error':"Bad Request - Invalid ID"},400)

    try:
        lpr = LprModelClass(id, lpr_mapping[id])
        lpd = LpdModelClass(id, lpd_mapping[id])
    except ValueError:
        return make_response({'error':"Model not found on triton server"},503)

    # Load input images
    files = request.files.to_dict(flat=False)['image']

    # Load filenames
    filenames = request.form.getlist('filename')

    output = check_request(request)

    if output!=True: return make_response(output,400)

    # Create directories for input and output images
    input_path, output_path = create_directories('lpdlprnet',id)

    #STATIC FILENAMES
    save_as = f"{output_path}/heatmap_{filenames[0]}"
    baseimage = f"{input_path}/{filenames[0]}"

    images = {}

    # Save input images --> for explain, only use 1st file
    images[filenames[0]] = files[0]
    files[0].save(baseimage)

    # SEND TO LPD
    lpd_response = lpd.predict(input_path)

    processed = {}
    reverse_mapping = {}
    i, info = 0, lpd_response[0]

    # DYNAMIC FILENAMES
    lpdout = f"{output_path}/exp_{info['file_name']}"
    demopic = f"{output_path}/overlay_lpdnet_{info['file_name']}"

    if info['HTTPStatus']==204:
        # No inference bounding box was found
        processed[i] = info
        save_image(images[info['file_name']], lpdout)
        reverse_mapping[f"exp_{info['file_name']}"] = i

    else:
        # info is a list of bbox, bbox is a dict containing a list (bbox)
        # and a single number, confidence score
        for j, bbox_info in enumerate(info["all_bboxes"]):
            crop_image(images[info['file_name']],bbox_info['bbox'],lpdout)
            reverse_mapping[f"exp_{info['file_name']}"] = i
            bbox_info[f"exp_bbox"] = bbox_info.pop('bbox')

    processed[i] = info

    # Call LPR on output of LPD
    lpr_response = lpr.predict(output_path)
    evaluate_lpd(model=lpd,image_path=baseimage, filename=filenames[0], id=id, overlay_path=save_as, num_segments=n, input_path=input_path)

    # Process response to return
    for lpr_info in lpr_response:
        file_name = lpr_info['file_name']
        index = file_name.split("_")[0]
        temp = {}
        temp['license_plate'] = list(lpr_info['license_plate'])
        temp['confidence_scores'] = lpr_info['confidence_scores']

    if id=='internal':
        render_image(images[info['file_name']],info['all_bboxes'], demopic)
        info['overlay_image'] = demopic

    # replace markdown placeholders with custom images
    image_replace = {
        '%placeholder1%' : f"{baseimage}",
        '%placeholder2%' : f"{demopic}",
        '%placeholder3%' : f"{lpdout}",
        '%placeholder4%' : f"{save_as}",
        '%placeholder5%' : pd.DataFrame(info['all_bboxes']).to_html(),
        '%placeholder6%' : pd.DataFrame(temp).assign(lp = '')[['lp', 'license_plate', 'confidence_scores']].rename(columns={'lp':lpr_info['license_plate']}).to_html(index=False, ),
    }



    return make_response({'explain_markdown': replace_in_markdown(image_replace, "/app/models/lpdlprnet/database/lpdlprnet_explainability_dynamic.md")},200)


def evaluate_lpd(model, filename, num_segments, id, image_path,  overlay_path,  input_path):
    import cv2, time

    lpd = model
    n = num_segments
    save_as = overlay_path

    now = datetime.datetime.now()

    create_directories('lpdnet',id)

    subimages = chop_image(image_path,  n)

    # Save input images
    for i, f in enumerate(subimages):
        cv2.imwrite(f"{input_path}/{str(i) + filename.split('.')[0] + '.png'}", f)

    lpd_response = lpd.predict(f"{input_path}")
    draw_confidence_heat_map(lpd_response, image_path, save_as, n)

    # delete subimages
    for i, f in enumerate(subimages):
        os.remove(f"{input_path}/{str(i) + filename.split('.')[0] + '.png'}")
