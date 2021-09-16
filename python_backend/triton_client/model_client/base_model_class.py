from abc import ABC, abstractmethod

class BaseModelClass(ABC):

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
    def get_status_input_schema(self):
        '''
        Returns the schema of the input required for status calls.
        '''
        pass

    @abstractmethod
    def get_status_output_schema(self):
        '''
        Returns the schema of the output of the status calls.
        '''
        pass
    
    @abstractmethod
    def predict(self):
        '''
        Returns the output of the model after inference.
        '''
        pass

    @abstractmethod
    def get_predict_input_schema(self):
        '''
        Returns the schema of the input required for predict calls.
        '''
        pass

    @abstractmethod
    def get_predict_output_schema(self):
        '''
        Returns the schema of the output of the predict calls.
        '''
        pass