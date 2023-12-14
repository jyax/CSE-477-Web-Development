# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app, jsonify
from flask import render_template, redirect, request, session, url_for, copy_current_request_context
from .utils.database.database import database
from werkzeug.datastructures import ImmutableMultiDict
from pprint import pprint
import json
import random
import functools
import requests

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
    email = form_fields['email']
    password = form_fields['password']
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
def piano():
    user_username = getUsername()
    return render_template('piano.html', user_username=user_username)


def daily_word():
    current_word = db.getDailyWord()
    if current_word is not None:
        return current_word['word']
    else:
        # Fetch a new word from the API
        response = requests.get("https://random-word-api.herokuapp.com/word")
        if response.status_code == 200:
            word_list = response.json()
            if word_list:
                current_word = word_list[0]
                # Store the new word in the database with today's date
                db.setDailyWord(word=current_word)
                return current_word
        else:
            print("Error fetching the word from the API")
            return None


def compare_guess(guess, current_daily_word):
    guess_letters = {}
    word_letters = {}
    loc = 0

    # Set up a nested dictionary for each letter of the guess that
    # holds the count and location of each letter
    for letter in guess:
        if letter not in guess_letters:
            guess_letters[letter] = {}
            guess_letters[letter]['count'] = 0
            guess_letters[letter]['location'] = []
        guess_letters[letter]['count'] += 1
        guess_letters[letter]['location'].append(loc)
        loc += 1

    # Similar as above
    loc = 0
    for letter in current_daily_word:
        if letter not in word_letters:
            word_letters[letter] = {}
            word_letters[letter]['count'] = 0
            word_letters[letter]['location'] = []
        word_letters[letter]['count'] += 1
        word_letters[letter]['location'].append(loc)
        loc += 1

    correctness = [0] * len(guess)
    loc = 0
    # Logic to check against the daily word
    for letter in guess_letters:
        correctness_type = 0
        if letter not in word_letters:
            loc += 1
            continue

        word_letters[letter]['count'] -= 1
        correctness_type += 1

        # Perform set intersection to find if any correct guessed locations
        guess_locations = set(guess_letters[letter]['location'])
        word_locations = set(word_letters[letter]['location'])
        common_locations = guess_locations.intersection(word_locations)

        if common_locations:
            correctness_type += 1
            list_of_correct_locations = list(common_locations)
            for location in list_of_correct_locations:
                correctness[location] = correctness_type
        correctness[loc] = correctness_type if correctness[loc] == 0 else correctness[loc]
        loc += 1
        if word_letters[letter]['count'] == 0:
            word_letters.pop(letter)

    return correctness


@app.route('/processguess', methods=['POST'])
def getdailyword():
    guess = request.form['guess']
    result = compare_guess(guess, daily_word())
    return jsonify(result)


@app.route('/wordly')
@login_required
def wordly():
    user_username = getUsername()
    return render_template('wordly.html', user_username=user_username)


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
