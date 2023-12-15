# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from datetime import datetime

from flask import current_app as app, jsonify
from flask import render_template, redirect, request, session, url_for, copy_current_request_context
from .utils.database.database import database
from apscheduler.schedulers.background import BackgroundScheduler
from pprint import pprint
import json
import random
import functools
import requests
import http.client
from urllib.parse import urlparse
import enchant
import atexit

db = database()

eDict = enchant.Dict("en-us")
#############
# Scheduler #
#############


def initial_clear():
    # Your session clearing logic goes here
    session.clear()


def clear_scores_table():
    db.query("DELETE FROM scores")


def daily_tasks():
    daily_word()
    clear_scores_table()
    session.clear()


scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(func=daily_tasks, trigger='cron', hour=0)  # Runs daily at midnight
scheduler.start()

atexit.register(lambda: scheduler.shutdown())

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


def getUsername():
    if 'email' in session:
        decrypted_email = db.reversibleEncrypt('decrypt', session['email'])
        user = db.getUserByEmail(decrypted_email)
        username = user['username'] if user else 'Unknown'
    else:
        username = 'Unknown'
    return username


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/processsignup', methods=['POST', 'GET'])
def processsignup():
    form_fields = dict((key, request.form.getlist(key)[0]) for key in list(request.form.keys()))
    username = form_fields['username']
    print(username)
    email = form_fields['email']
    print(email)
    password = form_fields['password']
    print(password)
    created = db.createUser(username, email, password)

    if created['success']:
        return json.dumps({'success': 1})
    else:
        return json.dumps({'success': 0, 'message': created['message']})


@app.route('/processlogin', methods=['POST', 'GET'])
def processlogin():
    form_fields = dict((key, request.form.getlist(key)[0]) for key in list(request.form.keys()))
    email = form_fields['email']
    password = form_fields['password']
    print(email)
    print(password)
    auth = db.authenticate(email, password)
    print(auth)
    if auth['success']:
        encrypted_email = db.reversibleEncrypt('encrypt', email)
        session['email'] = encrypted_email
        return json.dumps({'success': 1})

    else:
        return json.dumps({'success': 0, 'message': 'Invalid Credentials'})


@app.route('/logout')
def logout():
    session.pop('email', default=None)
    session.pop('first_login', default=None)
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
    user_username = getUsername()

    return render_template('home.html', fun_fact=x, user_username=user_username)


@app.route('/resume')
def resume():
    resume_data = db.getResumeData()
    pprint(resume_data)
    user_username = getUsername()
    return render_template('resume.html', resume_data=resume_data, user_username=user_username)


@app.route('/projects')
def projects():
    user_username = getUsername()
    return render_template('projects.html', user_username=user_username)


############
# Projects #
############
@app.route('/piano')
@login_required
def piano():
    user_username = getUsername()
    return render_template('piano.html', user_username=user_username)


def daily_word():
    current_word = db.getDailyWord()
    print(current_word)
    if current_word is not None:
        return current_word['word']
    else:
        print("Fetching new daily word...")
        # Fetch a new word from the API
        current_word = "?????????"
        while len(current_word) > 8:
            url = urlparse("https://random-word-api.herokuapp.com/word")
            conn = http.client.HTTPSConnection(url.netloc)
            conn.request("GET", url.path)
            response = conn.getresponse()
            if response.status == 200:
                word_list = json.loads(response.read().decode())
                if word_list:
                    current_word = word_list[0]
                    if validateword(current_word) and len(current_word) <= 8:
                        break
                    else:
                        current_word = "?????????"
            else:
                print("Error fetching the word from the API")
                return None
            conn.close()
        db.setDailyWord(word=current_word)
        return current_word


def compare_guess(guess, current_daily_word):
    # This list will hold the correctness of each letter in the guess
    correctness = [0] * len(guess)

    # First, let's mark all correct letters (right letter in the right place)
    for i, (g, w) in enumerate(zip(guess, current_daily_word)):
        if g == w:
            correctness[i] = 2  # Mark as correct
    print(f"Letters in correct spot: {correctness}")

    # Now, let's count the remaining letters in the daily word
    word_letters = {}
    for i, letter in enumerate(current_daily_word):
        if correctness[i] != 2:  # Only count letters that haven't been marked correct
            if letter not in word_letters:
                word_letters[letter] = 0
            word_letters[letter] += 1

    # Next, check for present letters (right letter in the wrong place)
    for i, letter in enumerate(guess):
        if correctness[i] == 0 and letter in word_letters and word_letters[letter] > 0:
            correctness[i] = 1  # Mark as present
            word_letters[letter] -= 1  # Decrement the count of this letter

    return correctness


def validateword(word):
    return eDict.check(word)


@app.route('/checkword', methods=['POST'])
def checkword():
    word_form = dict((key, request.form.getlist(key)[0]) for key in list(request.form.keys()))
    print(f"Request: {word_form}")
    print(f"Word to check: {word_form['word']}")
    word = validateword(word_form['word'])
    print(f"Valid word?: {word}")
    json_version = json.dumps({'word': word})
    print(f"JSON Return: {json_version}")
    return json_version


@app.route('/getlength', methods=['GET'])
def getlength():
    word_length = len(daily_word())
    print(f"Daily word is {daily_word()} with a length of {word_length}.")
    json_version = jsonify({'length': word_length})
    return json_version


@app.route('/processguess', methods=['POST'])
def processguess():
    guess_request = dict((key, request.form.getlist(key)[0]) for key in list(request.form.keys()))
    guess = guess_request['guess']
    result = compare_guess(guess, daily_word())
    if result == [2] * len(guess):
        return json.dumps({'correct': 1})
    else:
        return json.dumps({'correct': 0, 'result': result})


@app.route('/processscore', methods=['POST'])
def processscore():
    score_form = dict((key, request.form.getlist(key)[0]) for key in list(request.form.keys()))
    score = score_form['score']
    print(score)
    username = getUsername()
    print(username)
    created = db.setScore(score, username)
    if created['success']:
        return json.dumps({'success': 1})
    else:
        return json.dumps({'success': 0, 'message': created['message']})


@app.route('/processleaderboard', methods=['GET'])
def processleaderboard():
    leaderboard = db.getLeaderboard()

    json_version = jsonify({'leaderboard': leaderboard})
    return json_version


@app.route('/checkscore', methods=['GET'])
def checkscore():
    username = getUsername()
    print(f"Checking if {username} already has a score")
    score_exists = db.checkScore(username)
    print(f"Properly returned: {score_exists}")
    if score_exists:
        score = score_exists['score']
    else:
        score = None
    return json.dumps({'score': score})


@app.route('/wordly')
@login_required
def wordly():
    user_username = getUsername()
    first_login = session.get('first_login')
    if first_login is None:
        first_login = True
    print(f"First Login?: {first_login}")
    if first_login:
        print("Setting show instruction to true")
        show_instructions = True
        session['first_login'] = False
    else:
        print("Setting show instruction to false")
        show_instructions = False
    print(show_instructions)
    return render_template('wordly.html', user_username=user_username, show_instructions=show_instructions)


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
    user_username = getUsername()
    return render_template('processfeedback.html', feedback_list=feedback_list, user_username=user_username)
