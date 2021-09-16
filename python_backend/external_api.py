from app import app
from flask import request
from flask_cors import CORS, cross_origin
CORS(app)

@app.route('/api/lpdnet/',methods= ['POST', 'GET'])
def call_lpdnet():
    """
    This function responds to the external API call of obtaining
    lpdnet

    :return: JSON object 
    """
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
        imagefile = request.files.get('imagefile', '')
        print(imagefile, flush=True)
        return prediction   
    else:
        return {'code':404,'error':'Request not found'}
