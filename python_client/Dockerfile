FROM python:3.9

# Add the dependencies to the container and install the python dependencies
RUN pip install Pillow


WORKDIR /app
COPY requirements.txt .
RUN pip install nvidia-pyindex
RUN pip install tritonclient[all]
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
ENV VERSION="0.0.0"

# WORKDIR ./library
# RUN python setup.py --help 

# WORKDIR /app

CMD ["python", "api.py"]