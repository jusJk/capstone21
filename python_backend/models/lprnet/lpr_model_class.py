import os

import requests
from requests.exceptions import ConnectionError

from models.base_model_class import BaseModelClass
from .lpr_client import lpr_predict


class LprModelClass(BaseModelClass):

    def __init__(self, client_info, model_name):
        '''
        Instantiate the classes with the information of the 
        querying party -- corresponding to a specific triton
        model.
        '''
        url = os.environ.get('API_URL')
        BaseModelClass.__init__(self, client_info, url, model_name)
        self._mode = "Lprnet"
        self._class_list = "license_plate"
        if model_name=="lprnet_usa":
            self._mapping_output_file = "/app/triton_client/tao_triton/python/clustering_specs/us_lp_characters.txt"
        elif model_name=="lprnet_eu":
            self._mapping_output_file = "/app/triton_client/tao_triton/python/clustering_specs/eu_lp_characters.txt"
        else:
            raise ValueError("Model name is invalid -- no such model exists")

    # def status(self):
    #     '''
    #     Returns the status of the model
    #     '''
    #     try:
    #         triton_server_url = "http://" + self._url + "/v2/health/ready"
    #         response = requests.get(triton_server_url)
    #     except ConnectionError as error:
    #         return {'status': 'Inactive'}
    #     else:
    #         return {'status': 'Active'}

    def predict(self, file_path):
        '''
        Returns the output of the model after inference.
        '''
        if os.path.exists(file_path):
            return self._predict(file_path)
        else:
            return [{'HTTPStatus': 400,
                     'error': "File Path does not exist!"}]

    def _predict(self, file_path):
        number_files = len([name for name in os.listdir(
            file_path) if os.path.isfile(file_path+name)])
        print(number_files)
        if number_files < 256:
            self._batch_size = 8
        else:
            self._batch_size = 16
        return lpr_predict(model_name=self._model_name, mode=self._mode, class_list=self._class_list,
                           output_path="./",  url=self._url, image_filename=file_path, verbose=False,
                           streaming=False, async_set=False, protocol='HTTP', model_version="", batch_size=self._batch_size,
                           mapping_output_file=self._mapping_output_file )


if __name__ == "__main__":
    test_model = LprModelClass("hellosss")
    print(test_model.predict("../input/lpr/"))
