from app import app
from flask import request, send_file, make_response
from flask_cors import CORS, cross_origin
from utils.utils import create_directories, check_request, crop_image, render_image, save_image, filter_overlapping_bbox

import shutil
import json
import os
CORS(app)

from models.tcnet.trafficcamnet_model_class import TrafficCamNetModelClass
from models.lpdnet.lpd_model_class import LpdModelClass
from models.lprnet.lpr_model_class import LprModelClass

@app.route('/api/tclpdlprnet/<id>',methods= ['POST', 'GET'])
def call_tclpdlpr_combined(id):

    """
    This function responds to the external API call of obtaining
    traffic cam net
    :return: JSON object 
    """

    tc_mapping = json.load(open('/app/models/tclpdlprnet/database/tc_mapping.json'))
    lpd_mapping = json.load(open('/app/models/tclpdlprnet/database/lpd_mapping.json'))
    lpr_mapping = json.load(open('/app/models/tclpdlprnet/database/lpr_mapping.json'))
    LOGGING = True #Saves output images into the folders
    LPD_THRESHOLD = 0.6 #Threshold to filter images
    LPR_THRESHOLD = 0.6
    TCN_THRESHOLD = 0.6

    if (id not in lpd_mapping) or (id not in lpr_mapping)  or (id not in tc_mapping): 
        return make_response({'error':"Bad Request - Invalid ID"},400)

    try:
        tcn = TrafficCamNetModelClass(id, tc_mapping[id])
        lpr = LprModelClass(id, lpr_mapping[id])
        lpd = LpdModelClass(id, lpd_mapping[id])
    except ValueError:
        return make_response({'error':"Model not found on triton server"},503)

    if request.method=='GET':

        tc_status = tcn.status()
        lpd_status = lpd.status()
        lpr_status = lpr.status()

        if tc_status['status']=='Active' and lpd_status['status']=='Active' and lpr_status['status']=='Active':
            return make_response(tc_status,200)
        return make_response(tc_status,503)

    elif request.method=='POST':

        # Load input images
        files = request.files.to_dict(flat=False)['image']
        
        # Load filenames
        filenames = request.form.getlist('filename')

        output = check_request(request)

        if output!=True: return make_response(output,400)

        # Create directories for input and output images
        input_path, output_path = create_directories('tclpdlprnet',id)

        tcn_input = {}
        # Save input images
        for i, f in enumerate(files):
            tcn_input[filenames[i]] = f
            f.save(f"{input_path}/{filenames[i]}")

        # Call triton inference server
        try:
            tcn_response = tcn.predict(input_path)
        except FileNotFoundError:
            return make_response({'error':"Internal Server Error"},503)

        tcn_response = filter_overlapping_bbox(tcn_response)

        tcn_mapping = {}
        processed = {}
        # Process response to return
        for i, info in enumerate(tcn_response):
            if info['HTTPStatus']==204:
                # No inference car was found then save the image as is.
                
                save_image(tcn_input[info['file_name']],f"{output_path}/0_{info['file_name']}")
                
                tcn_mapping[f"0_{info['file_name']}"] = info['file_name']
                
                del info['HTTPStatus']

                processed[info['file_name']] = {'tcnet_response': info}

            else:
                # info is a list of bbox, bbox is a dict containing a list (bbox)
                # and a single number, confidence score
                for j, bbox_info in enumerate(info["all_bboxes"]):
                    
                    confidence_score=bbox_info['confidence_score']
                    if confidence_score < TCN_THRESHOLD:
                        del info["all_bboxes"][j]
                        continue
                    
                    crop_image(tcn_input[info['file_name']],bbox_info['bbox'],f"{output_path}/{j}_{info['file_name']}")
        
                    tcn_mapping[f"{j}_{info['file_name']}"] = info['file_name']
                
                del info['HTTPStatus']
                
                processed[info['file_name']] = {'tcnet_response': info} 
        
        #return {'test':[k for k in lpd_input.keys()]}

        # Call triton inference server
        try:
            lpd_response = lpd.predict(output_path)
        except FileNotFoundError:
            return make_response({'error':"Internal Server Error"},503)

        # Calculate IOU from among all permutations of bboxes for each image response and remove smaller box if iou > 0.1
        lpd_response = filter_overlapping_bbox(lpd_response)
        
        # Copy all the images from the output folder into input folder
        # So now only the output of lpd can be stored in output folder
        lpd_input = {}
        for f in os.listdir(output_path):
            shutil.move(f"{output_path}/{f}", input_path)
            lpd_input[f] = f"{input_path}/{f}" # this is because we copy over the outputs into the input folder


        # Save the lpd output images into a new folder
        lpd_mapping = {}
        
        for i, info in enumerate(lpd_response):
            if info['HTTPStatus']==204:
                # No inference bounding box was found

                del info['HTTPStatus']

                processed[tcn_mapping[info['file_name']]]['lpd_response'] = info 
            else:
                # info is a list of bbox, bbox is a dict containing a list (bbox)
                # and a single number, confidence score
                for j, bbox_info in enumerate(info["all_bboxes"]):
                    
                    confidence_score=bbox_info['confidence_score']
                    if confidence_score < LPD_THRESHOLD:
                        del info["all_bboxes"][j]
                        continue
                    
                    crop_image(lpd_input[info['file_name']],bbox_info['bbox'],f"{output_path}/{j}_{info['file_name']}")

                    lpd_mapping[f"{j}_{info['file_name']}"] = info['file_name'] #Tracking multiple bbox in an image

                    bbox_info[f"{j}_bbox"] = bbox_info.pop('bbox')

                del info['HTTPStatus']

                index = info['file_name'].split('_')[0]
                
                if 'lpd_response' in processed[tcn_mapping[info['file_name']]]:
                    processed[tcn_mapping[info['file_name']]]['lpd_response'][index] = info
                else:
                    processed[tcn_mapping[info['file_name']]]['lpd_response']= {index:info}
                

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
            print(file_name, flush=True)
            index_1 = file_name.split("_")[0] # lpd response identified more than one bbox in the same image
            index_2 = file_name.split("_")[1] # tcnet made 2 images so lpd response is twice

            # No license plate was detected -- filter it out
            if len(new_lp)==0:
                del processed[tcn_mapping[lpd_mapping[file_name]]]['lpd_response'][index_2]["all_bboxes"][int(index_1)]
            else:
                temp['license_plate'] = ''.join(new_lp)
                temp['confidence_scores'] = new_cs

                if 'lpr_response' in processed[tcn_mapping[lpd_mapping[file_name]]]:
                    processed[tcn_mapping[lpd_mapping[file_name]]]['lpr_response'][index_2] = temp
                else:
                    processed[tcn_mapping[lpd_mapping[file_name]]]['lpr_response'] = {index_2:temp}


        if id=='internal':
            
            for i, info in enumerate(lpd_response):
                if len(info["all_bboxes"])!=0:
                    render_image(lpd_input[info['file_name']],info["all_bboxes"],f"{output_path}/overlay_lpdnet_{info['file_name']}")
                    processed[tcn_mapping[info['file_name']]]['lpd_overlay_image'] = f"{output_path}/overlay_lpdnet_{info['file_name']}"
            
            for i, info in enumerate(tcn_response):
                if len(info["all_bboxes"])!=0:
                    render_image(tcn_input[info['file_name']],info["all_bboxes"],f"{output_path}/overlay_trafficcamnet_{info['file_name']}")
                    processed[info['file_name']]['tcn_overlay_image'] = f"{output_path}/overlay_trafficcamnet_{info['file_name']}"
        
        return make_response(processed,200)        