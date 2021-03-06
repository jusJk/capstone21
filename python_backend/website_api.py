from app import app
from database import model_info
import os
from flask import send_file, request, make_response

@app.route('/api/models/list')
def get_all_models():
    """
    This function responds to the interal API call of obtaining
    all models currently in the inference server

    :return: Dictionary//JSON 
    """
    info = {'models':[ 
                {
                'id': m, 
                'name': model_info.get(m).get('model_name'),
                'cover' : model_info.get(m).get('cover'),
                'status' : model_info.get(m).get('status')
                } 
            for m in model_info.keys()]}   
    return make_response(info,200)

@app.route('/api/info/<id>')
def get_model_info(id):  
    """
    This function responds to the interal API call of obtaining
    whether a model is active in the inference server
    
    :return: Dictionary//JSON 
    """ 
    
    if id in model_info: 
        return {id:model_info[id]}
    else:
        return make_response({'error':'invalid model name'},400)


@app.route('/api/get_image')
def get_image():
    file_path = request.args.get('path')
    if os.path.isfile(file_path):
        return send_file(file_path)
    else:
        return make_response({'error':'invalid file name'},400) 


@app.route('/api/get_md')
def get_md(): 
    file_path = request.args.get('path')
    if os.path.isfile(file_path):
        return send_file(file_path)
    else:
        return make_response({'error':'invalid file name'},400)

