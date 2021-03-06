from flask import Flask
import sys
sys.path.insert(1, '/app/triton_client/')

app = Flask(__name__)

from website_api import *
from models.lpdnet.api import *
from models.lprnet.api import *
from models.bpnet.api import *
from models.lpdlprnet.api import *
from models.tcnet.api import *
from models.tclpdlprnet.api import *

if __name__ == '__main__':
    test_bpnet()
    test_lpdnet()
    test_lprnet()
    test_tcnet()