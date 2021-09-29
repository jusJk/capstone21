from app import app
from flask import request, send_file
from flask_cors import CORS, cross_origin
from utils import crop_image, render_image, create_directories
import json
import os
from datetime import datetime
CORS(app)

import sys
sys.path.insert(1, 'triton_client/model_client')
from triton_client.model_client.lpd_model_class import LpdModelClass
from triton_client.model_client.lpr_model_class import LprModelClass
from triton_client.model_client.bodyposenet_model_class import BodyPoseNetClass


@app.route('/api/lpdnet/<id>',methods= ['POST', 'GET'])
def call_lpdnet(id):

    """
    This function responds to the external API call of obtaining
    lpdnet

    :return: JSON object 
    """
    
    lpd = LpdModelClass(id)

    if request.method=='GET':
        return lpd.status()
    
    elif request.method=='POST':

        # Create directories for input and output images
        now = datetime.now()
        curr_time = now.strftime("%d%m%y_%H%M%S")
        create_directories('lpdnet',id, curr_time)

        # Load input images
        # input_stream = request.files['image']
        files = request.files.to_dict(flat=False)['image']

        # Load filenames
        filenames = request.form.getlist('filename')
        
        images = {}
        # Save input images
        for i, f in enumerate(files):
            images[filenames[i]] = f
            f.save(f"triton_client/lpdnet/input/{id}/{curr_time}/{filenames[i]}")
        
        # Call triton inference server
        response = lpd.predict(f"triton_client/lpdnet/input/{id}/{curr_time}")
        
        # Process response to return
        processed = {}
        for i, info in enumerate(response):
            if info['HTTPStatus']==204:
                # No inference bounding box was found
                processed[i] = info
            else:
                # info is a list of bbox, bbox is a dict containing a list (bbox)
                # and a single number, confidence score
                for j, bbox_info in enumerate(info["all_bboxes"]):
                    crop_image(images[info['file_name']],bbox_info['bbox'],f"triton_client/lpdnet/output/{id}/{curr_time}/{j}_{info['file_name']}")
                    if id=='internal':
                        render_image(images[info['file_name']],bbox_info['bbox'],f"database/lpdnet/tmp/overlay_lpdnet_{info['file_name']}")
                        info['overlay_image'] = f"database/lpdnet/tmp/overlay_lpdnet_{info['file_name']}"
                processed[i] = info
        return processed        
    
    else:
        return {'code':404,'error':'Request not found'}
    

@app.route('/api/lprnet/<id>',methods= ['POST', 'GET'])
def call_lprnet(id):

    """
    This function responds to the external API call of obtaining
    lprnet

    :return: JSON object 
    """
    
    lpr = LprModelClass(id)

    if request.method=='GET':

        return lpr.status()
    
    elif request.method=='POST':

        # Create directories for input and output images
        now = datetime.now()
        curr_time = now.strftime("%H%M%S")
        create_directories('lprnet',id, curr_time)

        # Load input images
        # input_stream = request.files['image']
        files = request.files.to_dict(flat=False)['image']

        # Load filenames
        filenames = request.form.getlist('filename')
        
        images = {}
        # Save input images
        for i, f in enumerate(files):
            images[filenames[i]] = f
            f.save(f"triton_client/lprnet/input/{id}/{curr_time}/{filenames[i]}")
        
        # Call triton inference server
        response = lpr.predict(f"triton_client/lprnet/input/{id}/{curr_time}")
        
        # Process response to return
        processed = {}
        for i, info in enumerate(response):
            processed[i] = info
        return processed        
    
    else:
        return {'code':404,'error':'Request not found'}


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
                    
                    if id=='internal':
                        render_image(images[info['file_name']],bbox_info['bbox'],f"database/lpdnet/tmp/overlay_lpdnet_{info['file_name']}")
                        info['overlay_image'] = f"database/lpdnet/tmp/overlay_lpdnet_{info['file_name']}"
                    
                    bbox_info[f"{j}_bbox"] = bbox_info.pop('bbox')

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


@app.route('/api/bpnet/<id>',methods= ['POST', 'GET'])
def call_bpnet(id):

    """
    This function responds to the external API call of obtaining
    lpdnet

    :return: JSON object 
    """
    
    bpn = BodyPoseNetClass(id)

    if request.method=='GET':
        return bpn.status()
    
    elif request.method=='POST':

        # Create directories for input and output images
        now = datetime.now()
        curr_time = now.strftime("%d%m%y_%H%M%S")
        create_directories('bpnet',id, curr_time)

        # Load input images
        # input_stream = request.files['image']
        files = request.files.to_dict(flat=False)['image']

        # Load filenames
        filenames = request.form.getlist('filename')
        
        images = {}
        # Save input images
        for i, f in enumerate(files):
            images[filenames[i]] = f
            f.save(f"triton_client/bpnet/input/{id}/{curr_time}/{filenames[i]}")
        
        # Call triton inference server
        response = bpn.predict(f"triton_client/bpnet/input/{id}/{curr_time}")
        #return str(response['results'])
        # Process response to return
        processed = {}
        for file_name, info in response['results'].items():
            # info is a list of keypoints, keypoints is a dict containing a numpy array (coordinates)
            # and confidence score and a number total corresponding to the number of key points identified
            user_list = []
            for i, keypoints in enumerate(info):
                temp = {}
                for k, v in keypoints.items():
                    if k in ['total','score']:
                        temp[k] = v
                    else:
                        temp[k] = v.tolist()
                user_list.append(temp)
            processed[file_name] = user_list
        return processed        
    
    else:
        return {'code':404,'error':'Request not found'}