from flask import Flask

app = Flask(__name__)

from website_api import *
from external_api import *