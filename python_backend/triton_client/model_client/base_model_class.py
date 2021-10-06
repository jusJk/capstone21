from abc import ABC, abstractmethod

class BaseModelClass:

    '''
    Abstract class to enforce consistency across various model
    clients by having a certain set of functions that can be
    called by the backend.
    '''

    def __init__(self, client_info):
        '''
        Instantiate the classes with the information of the 
        querying party -- corresponding to a specific triton
        model.
        '''
        self._client_info = client_info
    
    @abstractmethod
    def status(self):
        '''
        Returns the status of the model
        '''
        pass

    
    @abstractmethod
    def predict(self):
        '''
        Returns the output of the model after inference.
        '''
        pass
