# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
from flask import render_template

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/<page>')
def route(page):
	return render_template(page)