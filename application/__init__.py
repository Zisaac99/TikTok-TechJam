# Purpose: Import Flask and set up the config

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#create the Flask app
app = Flask(__name__)
CORS(app)

# load configuration from config.cfg
app.config.from_pyfile('config.cfg')

# instantiate SQLAlchemy to handle db process
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = "/login"
login.login_message = u"Please log in to access this page."
login.login_message_category = "info"

#run the file routes.py
from application import routes