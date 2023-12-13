# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
from flask import render_template, redirect, request, session, url_for, copy_current_request_context
from .utils.database.database import database
from werkzeug.datastructures import ImmutableMultiDict
from pprint import pprint
import json
import random
import functools

db = database()


#################
# Login Related #
#################
def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "email" not in session:
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)
    return secure_function


def getUser():
    return session['email'] if 'email' in session else 'Unknown'


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/processsignup', methods=['POST', 'GET'])
def processsignup():
    form_fields = dict((key, request.form.getlist(key)[0]) for key in list(request.form.keys()))
    email = form_fields['email']
    password = form_fields['password']
    db.createUser(email, password)


@app.route('/processlogin', methods=['POST','GET'])
def processlogin():
    form_fields = dict((key, request.form.getlist(key)[0]) for key in list(request.form.keys()))
    email = form_fields['email']
    password = form_fields['password']

    auth = db.authenticate(email, password)
    
    if auth['success']:
        encrypted_email = db.reversibleEncrypt('encrypt', email)
        session['email'] = encrypted_email
        return json.dumps({'success': 1})
            #**redirect(url_for('home')))

    else:
        return json.dumps({'success': 0, 'message':  'Invalid Credentials'})

@app.route('/logout')
def logout():
    session.pop('email', default=None)
    return redirect('/')

################
# Other routes #
################
@app.route('/')
def root():
    return redirect('/home')


@app.route('/home')
def home():
    x = random.choice(
        ["I've been to pretty much every island in the Caribbean", "I play guitar", "My dad's side has a family band"])
    return render_template('home.html', fun_fact=x)


@app.route('/resume')
def resume():
    resume_data = db.getResumeData()
    pprint(resume_data)
    return render_template('resume.html', resume_data=resume_data)


@app.route('/projects')
def projects():
    return render_template('projects.html')

############
# Projects #
############
@app.route('/piano')
def piano():
    return render_template('piano.html')


@app.route('/wordly')
@login_required
def wordly():
    return render_template('wordly.html')

####################
# Feedback related #
####################
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
