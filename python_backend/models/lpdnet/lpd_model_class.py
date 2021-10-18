import os
import requests
from models.base_model_class import BaseModelClass
from .lpd_client import lpd_predict
from requests.exceptions import ConnectionError


class LpdModelClass(BaseModelClass):

    def __init__(self, client_info, model_name):
        '''
        Instantiate the classes with the information of the 
        querying party -- corresponding to a specific triton
        model.
        '''
        BaseModelClass.__init__(self, client_info)
        self._post_processing_config = "/app/triton_client/tao_triton/python/clustering_specs/clustering_config_lpdnet.prototxt"
        self._url = os.environ.get('API_URL')
        self._model_name = model_name
        self._mode = "DetectNet_v2"
        self._class_list = "license_plate"
        if model_name not in ['lpdnet_usa','lpdnet_eu']:
            raise ValueError("Model name is invalid -- no such model exists")

    def status(self):
        '''
        Returns the status of the model
        '''
        try:
            triton_server_url = "http://" + self._url + "/v2/health/ready"
            response = requests.get(triton_server_url)
        except ConnectionError as error:
            return {'status': 'Inactive'}
        else:
            return {'status': 'Active'}

    def predict(self, file_path):
        '''
        Returns the output of the model after inference.
        '''
        if os.path.exists(file_path):
            return self._predict(file_path)
        else:
            raise FileNotFoundError("File Path does not exist!")

    def _predict(self, file_path):
        number_files = len([name for name in os.listdir(
            file_path) if os.path.isfile(file_path+name)])
        if number_files < 256:
            self._batch_size = 8
        else:
            self._batch_size = 16
        return lpd_predict(model_name=self._model_name, mode=self._mode, class_list=self._class_list,
                           output_path="./", postprocessing_config=self._post_processing_config,
                           url=self._url, image_filename=file_path, verbose=False, streaming=False, async_set=True,
                           protocol='HTTP', model_version="", batch_size=self._batch_size)

# To handle output_path
if __name__ == "__main__":
    test_model = LpdModelClass("hellosss")
    # print(test_model.status())
    print(test_model.predict("../input/lpd"))
