import os

import requests
from requests.exceptions import ConnectionError

from base_model_class import BaseModelClass
from lpr_client import lpr_predict


class LprModelClass(BaseModelClass):

    def __init__(self, client_info):
        '''
        Instantiate the classes with the information of the 
        querying party -- corresponding to a specific triton
        model.
        '''
        BaseModelClass.__init__(self, client_info)
        self._url = "35.240.147.255:6000"
        self._model_name = "lprnet_usa"
        self._mode = "Lprnet"
        self._class_list = "license_plate"
        self.mapping_output_file = "/app/triton_client/postprocessing_config/us_lp_characters.txt"
    
    def status(self):
        '''
        Returns the status of the model
        '''
        try:
            triton_server_url = "http://" + self._url + "/v2/health/ready"
            response = requests.get(triton_server_url)
        except ConnectionError as error:
            return {'HTTPStatus' : 503, 'status':'Inactive'}
        else:
            return {'HTTPStatus' : 200, 'status':'Active'}
                
    def predict(self, file_path):
        '''
        Returns the output of the model after inference.
        '''
        if os.path.exists(file_path):
            return self._predict(file_path)
        else:
            return [{'HTTPStatus':400, 
                    'error':"File Path does not exist!"}]

    def _predict(self, file_path):
        number_files = len([name for name in os.listdir(file_path) if os.path.isfile(file_path+name)])
        print(number_files)
        if number_files < 256:
            self._batch_size = 8
        else:
            self._batch_size = 32
        return lpr_predict(model_name = self._model_name, mode = self._mode, class_list = self._class_list, \
                            output_path = "./",  url = self._url, image_filename = file_path, verbose = False, \
                                streaming = False, async_set = False, protocol = 'HTTP', model_version = "", batch_size = self._batch_size, \
                                mapping_output_file = "/app/triton_client/postprocessing_config/us_lp_characters.txt")

if __name__ == "__main__":
    test_model = LprModelClass("hellosss")
    print(test_model.predict("../input/lpr/"))

