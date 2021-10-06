FROM nvcr.io/nvidia/tritonserver:21.07-py3
WORKDIR /app

COPY . .

EXPOSE 8080

RUN bash fetch_models.sh

EXPOSE 8000
EXPOSE 8001
EXPOSE 8002

ENTRYPOINT ["tritonserver", "--model-repository=model_repository"]

# # Nvidia Triton Inference Server as base image
# FROM nvcr.io/nvidia/tritonserver:21.07-py3

# # Go to home directory and paste examples folder (contains model_repository and fetch_models.sh)
# WORKDIR /
# COPY ./examples examples

# # Pull the model definitions
# RUN bash /examples/fetch_models.sh

# WORKDIR /opt/tritonserver
# ENTRYPOINT ["tritonserver", "--model-repository=/examples/model_repository"]