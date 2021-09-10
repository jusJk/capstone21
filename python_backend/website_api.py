from app import app

@app.route('/api/models/list')
def get_all_models():
    """
    This function responds to the interal API call of obtaining
    all models currently in the inference server

    :return: JSON object 
    """
    models = {'1':'lpdnet', '2':'lprnet'}

    return models

@app.route('/api/info/<id>')
def get_model_info(id):
    """
    This function responds to the interal API call of obtaining
    whether a model is active in the inference server
    :return: JSON object 
    """
    models = {'lpdnet':{'is_active':True}, 'lprnet':{'is_active':False}}
    if id in models:
        return {id:models[id]}
    else:
        return {'error':'invalid model name'}
