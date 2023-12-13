# Author: Prof. MM Ghassemi <ghassem3@msu.edu>

#--------------------------------------------------
# Import Requirements
#--------------------------------------------------
import os
from flask import Flask
from flask_failsafe import failsafe
from .utils.database.database import database
import secrets

#--------------------------------------------------
# Create a Failsafe Web Application
#--------------------------------------------------
@failsafe
def create_app(debug=False):
	app = Flask(__name__)

	app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
	app.debug = debug

	app.secret_key = 'AKWNF1231082fksejfOSEHFOISEHF24142124124124124iesfhsoijsopdjf'

	db = database()
	db.createTables(purge=True)

	db.createUser(email='owner@email.com', password='password', role='owner')
	db.createUser(email='guest@email.com', password='password', role='guest')

	with app.app_context():
		from . import routes
		return app
