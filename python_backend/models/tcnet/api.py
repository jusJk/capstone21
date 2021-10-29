from app import app
from flask import request, send_file, make_response
from flask_cors import CORS, cross_origin
from utils.utils import create_directories, check_request, crop_image, render_image, filter_overlapping_bbox

import json
import os
CORS(app)

from .trafficcamnet_model_class import TrafficCamNetModelClass

@app.route('/api/tcnet/<id>',methods= ['POST', 'GET'])
def call_trafficcamnet(id):

    """
    This function responds to the external API call of obtaining
    traffic cam net
    :return: JSON object 
    """

    mapping = json.load(open('/app/models/tcnet/database/mapping.json'))
    LOGGING = True #Saves output images into the folders
    THRESHOLD = 0.6 #Threshold for bbox to be tuned

    if id not in mapping: return make_response({'error':"Bad Request - Invalid ID"},400)

    model_name=mapping[id]

    try:
        tcn = TrafficCamNetModelClass(id,model_name)
    except ValueError:
        return make_response({'error':"Model not found on triton server"},503)

    if request.method=='GET':
        status = tcn.status()
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
        input_path, output_path = create_directories('tcnet',id)

        images = {}
        # Save input images
        for i, f in enumerate(files):
            images[filenames[i]] = f
            f.save(f"{input_path}/{filenames[i]}")

        # Call triton inference server
        try:
            response = tcn.predict(input_path)
        except FileNotFoundError:
            return make_response({'error':"Internal Server Error"},503)

        response = filter_overlapping_bbox(response)

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
                        del info["all_bboxes"][j]
                        continue
                
                if id=='internal':
                    render_image(images[info['file_name']],info["all_bboxes"],f"{output_path}/overlay_trafficcamnet_{info['file_name']}")
                    info['overlay_image'] = f"{output_path}/overlay_trafficcamnet_{info['file_name']}"
                
                del info['HTTPStatus']

                processed[i] = info
        
        return make_response(processed,200)        