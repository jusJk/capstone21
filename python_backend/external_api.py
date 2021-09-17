from app import app
from flask import request, send_file
from flask_cors import CORS, cross_origin
from utils import crop_image, render_image
import json
import os
from datetime import datetime
from io import BytesIO
CORS(app)

import sys
sys.path.insert(1, 'triton_client/model_client')
from triton_client.model_client.lpd_model_class import LpdModelClass

@app.route('/api/lpdnet/<id>',methods= ['POST', 'GET'])
def call_lpdnet(id):
    """
    This function responds to the external API call of obtaining
    lpdnet

    :return: JSON object 
    """
    lpd = LpdModelClass(id)
    model_status = {
                    'code':200,
                    'status':'active'
                    }

    if request.method=='GET':
        return model_status
    
    elif request.method=='POST':
        # Create directories for input and output images
        now = datetime.now()
        curr_time = now.strftime("%H%M%S")
        if os.path.isdir(f"triton_client/input/{id}/"):
            os.mkdir(f"triton_client/input/{id}/{curr_time}")
            os.mkdir(f"triton_client/output/{id}/{curr_time}")
        else:
            os.mkdir(f"triton_client/input/{id}")
            os.mkdir(f"triton_client/output/{id}")
            os.mkdir(f"triton_client/input/{id}/{curr_time}")
            os.mkdir(f"triton_client/output/{id}/{curr_time}")

        # Load input images
        # input_stream = request.files['image']
        files = request.files.to_dict(flat=False)['image']

        # Load filenames
        filenames = request.form.getlist('filename')
        
        images = {}
        # Save input images
        for i, f in enumerate(files):
            images[filenames[i]] = f
            f.save(f"triton_client/input/{id}/{curr_time}/{filenames[i]}")
        
        # Call triton inference server
        response = lpd.predict(f"triton_client/input/{id}/{curr_time}")
        
        # Process response to return
        processed = {}
        for i, info in enumerate(response):
            # crop_image(images[info['file_name']],info['bbox'],f"triton_client/output/{id}/{curr_time}/{info['file_name']}")
            if id=='internal':
                overlayed_image = render_image(images[info['file_name']],info['bbox'],f"static/overlay_lpdnet_{info['file_name']}")
                info['overlay_image'] = f"static/overlay_lpdnet_{info['file_name']}"
            processed[i] = info
        return processed        
    
    else:
        return {'code':404,'error':'Request not found'}
