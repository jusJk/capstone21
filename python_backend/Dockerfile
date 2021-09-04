FROM python:3.7

# set working directory
WORKDIR /app

# Add the dependencies to the container and install the python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
ENV VERSION="0.0.0"

# WORKDIR ./library
# RUN python setup.py --help 

# WORKDIR /app

CMD ["flask", "run"]