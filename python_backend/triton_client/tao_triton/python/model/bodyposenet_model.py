import os

import tritonclient.grpc as grpcclient
import tritonclient.grpc.model_config_pb2 as mc
import tritonclient.http as httpclient
from tritonclient.utils import InferenceServerException
from tritonclient.utils import triton_to_np_dtype

from tao_triton.python.model.triton_model import TritonModel


class BodyPoseNetModel(TritonModel):

    def __init__(self, max_batch_size, input_names, output_names,
                 channels, height, width, data_format, triton_dtype):
        """Set up a BodyPoseNet triton model instance.
        
        Args:
            max_batch_size(int): The maximum batch size of the TensorRT engine.
            input_names (str): List of the input node names
            output_names (str): List of the output node names
            channels (int): Number of chanels in the input dimensions
            height (int): Height of the input
            width (int): Width of the input
            data_format (str): The input dimension order. This can be "channels_first"
                or "channels_last". "channels_first" is in the CHW order,
                and "channels_last" is in HWC order.
            triton_dtype (proto): Triton input data type.
            channel_mode (str): String order of the C dimension of the input.
                "RGB" or "BGR"
                
        Returns:
            An instance of the DetectnetModel.
        """
        
        super().__init__(max_batch_size, input_names, output_names,
                         channels, height, width, data_format,
                         triton_dtype)
        self.scale = 1. / 255.0

    @staticmethod
    def parse_model(model_metadata, model_config):
        """Simple class to parse model metadata and model config."""
        if len(model_metadata.inputs) != 1:
            raise Exception("expecting 1 input, got {}".format(
                len(model_metadata.inputs)))

        if len(model_metadata.outputs) != 2:
            raise Exception("expecting 2 output, got {}".format(
                len(model_metadata.outputs)))

        if len(model_config.input) != 1:
            raise Exception(
                "expecting 1 input in model configuration, got {}".format(
                    len(model_config.input)))

        if len(model_config.output) != 2:
            raise Exception(
                "expecting 2 outputs in model configuration, got {}".format(
                    len(model_config.output)))

        input_metadata = model_metadata.inputs[0]
        input_config = model_config.input[0]
        output_metadata = model_metadata.outputs

        for data in output_metadata:
            if (data.datatype != "FP32"):
                raise Exception("expecting output datatype to be FP32, model '" +
                                data.name + "' output type is " +
                                data.datatype)

        # Model input must have 3 dims, either CHW or HWC (not counting
        # the batch dimension), either CHW or HWC
        input_batch_dim = (model_config.max_batch_size > 0)
        expected_input_dims = 3 + (1 if input_batch_dim else 0)
        if len(input_metadata.shape) != expected_input_dims:
            raise Exception(
                "expecting input to have {} dimensions, model '{}' input has {}".
                format(expected_input_dims, model_metadata.name,
                    len(input_metadata.shape)))

        if type(input_config.format) == str:
            FORMAT_ENUM_TO_INT = dict(mc.ModelInput.Format.items())
            print(FORMAT_ENUM_TO_INT)
            input_config.format = FORMAT_ENUM_TO_INT[input_config.format]

        if ((input_config.format != mc.ModelInput.FORMAT_NCHW) and
            (input_config.format != mc.ModelInput.FORMAT_NHWC)):
            raise Exception("unexpected input format " +
                            mc.ModelInput.Format.Name(input_config.format) +
                            ", expecting " +
                            mc.ModelInput.Format.Name(mc.ModelInput.FORMAT_NCHW) +
                            " or " +
                            mc.ModelInput.Format.Name(mc.ModelInput.FORMAT_NHWC))

        if input_config.format == mc.ModelInput.FORMAT_NHWC:
            h = input_metadata.shape[1 if input_batch_dim else 0]
            w = input_metadata.shape[2 if input_batch_dim else 1]
            c = input_metadata.shape[3 if input_batch_dim else 2]
        else:
            c = input_metadata.shape[1 if input_batch_dim else 0]
            h = input_metadata.shape[2 if input_batch_dim else 1]
            w = input_metadata.shape[3 if input_batch_dim else 2]

        # This part should be be where the input and output names are returned.
        return (model_config.max_batch_size, input_metadata.name,
                [data.name for data in output_metadata], c, h, w, input_config.format,
                input_metadata.datatype)
