from abc import ABC, abstractmethod
import json
import os
import requests

class BaseModelClass:

    '''
    Abstract class to enforce consistency across various model
    clients by having a certain set of functions that can be
    called by the backend.
    '''

    def __init__(self, client_info, url, model_name):
        '''
        Instantiate the classes with the information of the 
        querying party -- corresponding to a specific triton
        model.
        '''
        self._client_info = client_info
        self._url = url
        self._model_name = model_name
    
    def status(self):
        '''
        Returns the status of the model
        '''
        triton_server_url = f'http://{self._url}/v2/repository/index'
        try:
            response = requests.post(triton_server_url)
            body = json.loads(response.text)
        except ConnectionError:
            return {'status': 'Inactive'}
        
        model = list(filter(lambda model: model['name'] == self._model_name, body))
        if model:
            state = model[0]['state']
            if state == 'READY':
                return {'status': 'Active'}
            else:
                return {'status': 'Inactive'}
        else:
            return {'status': 'Model not found'}   

    
    @abstractmethod
    def predict(self):
        '''
        Returns the output of the model after inference.
        '''
        pass
