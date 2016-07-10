# Import the Flask Framework
import os
import sys

# This is necessary so other directories can find the lib folder
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
from saylua import app
