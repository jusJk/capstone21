from app import app
from flask import request
from flask_cors import CORS, cross_origin
import json
CORS(app)

import sys
sys.path.insert(1, 'triton_client/model_client')
from triton_client.model_client.lpd_model_class import LpdModelClass


@app.route('/api/lpdnet/',methods= ['POST', 'GET'])
def call_lpdnet():
    """
    This function responds to the external API call of obtaining
    lpdnet

    :return: JSON object 
    """
    lpd = LpdModelClass('dummy')   
    model_status = {
                    'code':200,
                    'status':'active'
                    }
    prediction = {
                'code':200,
                'bounding_box':[0,120,100,10],
                'confidence_score':0.98
                }

    if request.method=='GET':
        return model_status
    
    elif request.method=='POST':
        # Load input images
        # input_stream = request.files['image']
        files = request.files.to_dict(flat=False)['image']

        # Load filenames
        filenames = request.form.getlist('filename')
        
        # Save input images
        for i, f in enumerate(files):
            f.save(f"triton_client/input/test/{filenames[i]}")
        
        # Call triton inference server
        response = lpd.predict("triton_client/input/test/")
        
        # Process response to return
        processed = {}
        for i, info in enumerate(response):
            processed[i] = info
        return processed
    
    else:
        return {'code':404,'error':'Request not found'}
