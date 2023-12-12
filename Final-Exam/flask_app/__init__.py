# Author: Prof. MM Ghassemi <ghassem3@msu.edu>

#--------------------------------------------------
# Import Requirements
#--------------------------------------------------
import os
from flask import Flask
from flask_failsafe import failsafe
from flask_bcrypt import Bcrypt
from .utils.database.database import database
import secrets

#--------------------------------------------------
# Create a Failsafe Web Application
#--------------------------------------------------
@failsafe
def create_app():
	app = Flask(__name__)
	app.secret_key = secrets.token_hex(16)

	bcrypt = Bcrypt(app)
	db = database(bcrypt)
	db.createTables(purge=True)

	with app.app_context():
		from . import routes
		return app
