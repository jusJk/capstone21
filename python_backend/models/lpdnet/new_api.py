# Think of this as a template file
from app import app
from flask import request, send_file
from flask_cors import CORS, cross_origin
from utils.utils import crop_image, render_image, create_directories, save_image, check_request

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
    mapping = json.load(open('lpdnet.json'))
    LOGGING = True #Saves output images into the folders
    THRESHOLD = 0.9 #Threshold for bbox to be tuned

    if id not in mapping: return {'code':404, 'error':"Id not found"}

    model_name=mapping[id]

    lpd = LpdModelClass(id,model_name)

    if request.method=='GET':
        return lpd.status()
    
    elif request.method=='POST':

        output = check_request(request)

        # Create directories for input and output images
        create_directories()
        
        save_images()
        
        # Call triton inference server
        lpd.predict()
        
        check_response()

        process_response()
        
        return processed        
    
    else:
        return {'code':404,'error':'Request not found'}