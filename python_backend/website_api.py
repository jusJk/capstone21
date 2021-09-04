from flask import Flask
import json

app = Flask(__name__)

@app.route('/api/models/')
def get_all_models():
    """
    This function responds to the interal API call of obtaining
    all models currently in the inference server

    :return: JSON object 
    """
    models = {'1':'Model 1', '2':'Model 2'}

    return models

@app.route('/api/models/<id>')
def get_model_info(id):
    """
    This function responds to the interal API call of obtaining
    all models currently in the inference server

    :return: JSON object 
    """
    models = {'1':'Model 1', '2':'Model 2'}

    return {id:models[id]}
