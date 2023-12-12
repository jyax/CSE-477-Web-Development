# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
from flask import render_template, redirect, request, session, url_for, copy_current_request_context
from .utils.database.database import database
from werkzeug.datastructures import ImmutableMultiDict
from pprint import pprint
import json
import random
from flask import url_for

db = database()


@app.route('/')
def root():
    return redirect('/home')


@app.route('/home')
def home():
    x = random.choice(
        ["I've been to pretty much every island in the Caribbean", "I play guitar", "My dad's side has a family band"])
    return render_template('home.html', fun_fact=x)


@app.route('/login', methods=['POST'])
def login():
    return render_template('login.html')

@app.route('/processlogin', methods=['POST'])
def processlogin():
    email = request.form.get['email']
    password = request.form.get['password']

    auth = db.authenticate(email, password)
    
    if auth['success']:
        session['user_email']
        return redirect(url_for('home'))

@app.route('/resume')
def resume():
    resume_data = db.getResumeData()
    pprint(resume_data)
    return render_template('resume.html', resume_data=resume_data)


@app.route('/projects')
def projects():
    return render_template('projects.html')


@app.route('/piano')
def piano():
    return render_template('piano.html')


@app.route('/wordly')
def wordly():
    return render_template('wordly.html')


@app.route('/submitfeedback', methods=['POST'])
def processfeedback():
    # Insert given feedback into table
    name = request.form.get('name')
    email = request.form.get('email')
    comment = request.form.get('comment')

    db.insertRows('feedback', ['name', 'email', 'comment'], parameters=[[name, email, comment]])

    return redirect(url_for('feedback'))


@app.route('/feedback')
def feedback():
    # Retrieve all given feedback
    retrieve_feedback = "SELECT * FROM feedback"
    feedback_list = db.query(retrieve_feedback)
    return render_template('processfeedback.html', feedback_list=feedback_list)
