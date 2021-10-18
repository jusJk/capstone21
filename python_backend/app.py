from flask import Flask

app = Flask(__name__)

from website_api import *
from external_api import *
from models.lpdnet.api import *
from models.lprnet.api import *
from models.bpnet.api import *
from models.lpdlprnet.api import *