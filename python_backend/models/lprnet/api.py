from app import app
from flask import request, send_file, make_response
from flask_cors import CORS, cross_origin
from utils.utils import create_directories, check_request

import json
import os
CORS(app)

from .lpr_model_class import LprModelClass

@app.route('/api/lprnet/<id>',methods= ['POST', 'GET'])
def call_lprnet(id):

    """
    This function responds to the external API call of obtaining
    lprnet

    :return: JSON object
    """

    mapping = json.load(open('/app/models/lprnet/database/mapping.json'))
    LOGGING = True #Saves output images into the folders
    THRESHOLD = 0.6 #Threshold to filter images

    if id not in mapping: return make_response({'error':"Bad Request - Invalid ID"},400)

    model_name=mapping[id] 

    try:
        lpr = LprModelClass(id,model_name)
    except ValueError:
        return make_response({'error':"Model not found on triton server"},503)

    if request.method=='GET':
        status = lpr.status()
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
        input_path, output_path = create_directories('lprnet',id)

        images = {}
        # Save input images
        for i, f in enumerate(files):
            images[filenames[i]] = f
            f.save(f"{input_path}/{filenames[i]}")

        # Call triton inference server
        try:
            response = lpr.predict(input_path)
        except FileNotFoundError:
            return make_response({'error':"Internal Server Error"},503)

        # Process response to return
        processed = {}
        for i, info in enumerate(response):
            confidence_scores = info['confidence_scores'] #List of confidence scores
            license_plate = info['license_plate']

            new_lp = [char for i, char in enumerate(license_plate) if confidence_scores[i]> THRESHOLD]
            new_cs = [c for c in confidence_scores if c > THRESHOLD]

            info['license_plate'] = ''.join(new_lp)
            info['confidence_scores'] = new_cs

            del info['HTTPStatus']

            processed[i] = info

        return make_response(processed,200)

def test_lprnet():
    id='internal'
    mapping = json.load(open('/app/models/lprnet/database/mapping.json'))
    model = LprModelClass(id, mapping[id])
    print('LPRnet: ', model.status())