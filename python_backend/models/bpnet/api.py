from app import app
from flask import request, send_file, make_response
from flask_cors import CORS, cross_origin
from utils.utils import create_directories, check_request, plot_keypoints, replace_in_markdown
from models.bpnet.bpnetutils import evaluate_bpnet

import json
import os
import pandas as pd
CORS(app)

from .bodyposenet_model_class import BodyPoseNetClass

@app.route('/api/bpnet/<id>',methods= ['POST', 'GET'])
def call_bpnet(id):

    """
    This function responds to the external API call of obtaining
    bpnet

    :return: JSON object
    """

    mapping = json.load(open('/app/models/bpnet/database/mapping.json'))
    LOGGING = True #Saves output images into the folders
    THRESHOLD = 0.6 #Threshold to filter images

    if id not in mapping: return make_response({'error':"Bad Request - Invalid ID"},400)

    try:
        bpn = BodyPoseNetClass(id, mapping[id])
    except ValueError:
        return make_response({'error':"Model not found on triton server"},503)

    if request.method=='GET':
        status = bpn.status()
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
        input_path, output_path = create_directories('bpnet',id)

        images = {}
        # Save input images
        for i, f in enumerate(files):
            images[filenames[i]] = f
            f.save(f"{input_path}/{filenames[i]}")

        # Call triton inference server
        try:
            response = bpn.predict(input_path)
        except FileNotFoundError:
            return make_response({'error':"Internal Server Error"},503)

        # Process response to return
        processed = {}
        for file_name, info in response['results'].items():
            # info is a list of keypoints corresponding to number of people identified
            # keypoints is a dict containing a numpy array (coordinates)
            # and confidence score and a number "total"
            # corresponding to the number of key points identified
            user_list = {}
            for i, keypoints in enumerate(info):
                temp = {}
                for k, v in keypoints.items():
                    if k in ['total','score']:
                        temp[k] = v
                    else:
                        temp[k] = v.tolist()
                user_list[str(i)] = temp
            processed[file_name] = user_list

            if id=='internal':
                output_path = f"{output_path}/{file_name}"
                plot_keypoints(response,file_name,f"{input_path}/{file_name}",output_path)
                processed[file_name]['overlay_image'] = output_path

            # del info['HTTPStatus']

        return make_response(processed,200)



@app.route('/api/bpnet/explain/<id>',methods= ['POST', 'GET'])
def call_explain_bpnet(id):

    """
    This function responds to the external API call of explaining
    bpnet

    :return: JSON object
    """

    mapping = json.load(open('/app/models/bpnet/database/mapping.json'))
    LOGGING = True #Saves output images into the folders
    THRESHOLD = 0.6 #Threshold to filter images

    if id not in mapping: return make_response({'error':"Bad Request - Invalid ID"},400)

    try:
        bpn = BodyPoseNetClass(id, mapping[id])
    except ValueError:
        return make_response({'error':"Model not found on triton server"},503)

    if request.method=='GET':
        status = bpn.status()
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
        input_path, output_path = create_directories('bpnet',id)
        

        images = {}
        # Save input images
        for i, f in enumerate(files):
            images[filenames[i]] = f
            f.save(f"{input_path}/{filenames[i]}")
            # enforce 1 image only
            break
        
        save_as = f"{output_path}/heatmap_{filenames[0]}"

        # Call triton inference server
        try:
            response = bpn.predict(input_path, return_tensor=True)
            tensors = response.get('tensor_response')[0]
            hm1, hm2, paf1, paf2 = evaluate_bpnet(f"{input_path}/{filenames[0]}",
                tensors.get(filenames[0]).get('heatmap'),
                tensors.get(filenames[0]).get('paf'),
                output_path, filenames[0]
            )
        except FileNotFoundError:
            return make_response({'error':"Internal Server Error"},503)

        # Process response to return
        processed = {}
        for file_name, info in response['results'].items():
            # info is a list of keypoints corresponding to number of people identified
            # keypoints is a dict containing a numpy array (coordinates)
            # and confidence score and a number "total"
            # corresponding to the number of key points identified
            user_list = {}
            for i, keypoints in enumerate(info):
                temp = {}
                for k, v in keypoints.items():
                    if k in ['total','score']:
                        temp[k] = v
                    else:
                        temp[k] = v.tolist()
                user_list[str(i)] = temp
            processed[file_name] = user_list

            if id=='internal':
                output_path = f"{output_path}/{file_name}"
                plot_keypoints(response,file_name,f"{input_path}/{file_name}",output_path)
                processed[file_name]['overlay_image'] = output_path

            # del info['HTTPStatus']
        
        image_replace = {
            '%placeholder1%' : f"{input_path}/{filenames[0]}", 
            '%placeholder2a%' : hm1,
            '%placeholder2b%' : hm2,
            '%placeholder2c%' : paf1,
            '%placeholder2d%' : paf2,
            '%placeholder3%' : pd.DataFrame(processed.get(filenames[0]).get('0')).assign(coordinate=['x', 'y']).set_index('coordinate').drop(['score','total'], axis=1).T.to_html(),
            '%placeholder4%' : f"{output_path}", 
        }
    
    
        return {'explain_markdown': replace_in_markdown(image_replace, "models/bpnet/database/bpnet_explainability_dynamic.md")}        
    

        return make_response(processed,200)



def test_bpnet():
    id='internal'
    mapping = json.load(open('/app/models/bpnet/database/mapping.json'))
    model = BodyPoseNetClass(id, mapping[id])
    print('BPnet: ', model.status())
