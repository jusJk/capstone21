FROM python:3.7

# COPY ./triton_client /triton_client 
# WORKDIR /triton_client

# RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8002

# set working directory
WORKDIR /app

# Add the dependencies to the container and install the python dependencies
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
# Dependency for OpenCV
RUN apt-get update && apt-get install -y libgl1 
EXPOSE 5000
ENV VERSION="0.0.0"

CMD ["flask", "run", "--host=0.0.0.0"]
# CMD ["/bin/bash"]