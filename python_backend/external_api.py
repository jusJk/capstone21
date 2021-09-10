from app import app
from flask import request

@app.route('/api/lpdnet/',methods= ['POST', 'GET'])
def call_lpdnet():
    """
    This function responds to the external API call of obtaining
    lpdnet

    :return: JSON object 
    """
    model_status='active'
    prediction = {'bounding_box':[0,120,100,10],
                'confidence_score':0.98
                }
    if request.method=='GET':
        return {'status':model_status}
    elif request.method=='POST':
        return prediction
    else:
        return {'error':'invalid api call'}
