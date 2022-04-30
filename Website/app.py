from asyncio.windows_events import NULL
from matplotlib.pyplot import get
import pyrebase
from flask import render_template, request, redirect, session, Flask, url_for
import sys, os

from sympy import Q
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from API import api

# YOU CAN ONLY RUN THE APPLICATION FROM HERE


config = {
    "apiKey": "AIzaSyDW6j3T5zqNfpRHQrYZXk12hICYbzZzoxk",
    "authDomain": "iiqw-2ab5f.firebaseapp.com",
    "databaseURL": "https://iiqw-2ab5f-default-rtdb.firebaseio.com/",
    "projectId": "iiqw-2ab5f",
    "storageBucket": "iiqw-2ab5f.appspot.com",
    "messagingSenderId": "260325577865",
    "appId": "1:260325577865:web:a1969fa00e43030955e258"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

# Argument is the name of the application's module or package. __name__ is a convenient shortcut for this.
# This is needed so flask knows where to look for resources such as templates and static files.
app = Flask(__name__)


# Use route() to tell flask what url should trigger our function
# The below function returns the html file we want to display in the user's browser
# Default content type is HTML
@app.route("/", methods=['GET'])
def home():
    try:
        rand_quotes = api.get_random_quote()
        return render_template('home.html', rand_quotes = rand_quotes)
    except:
        return render_template('home.html')


@app.route("/quote", methods=['GET', 'POST'])
def quote():
    if request.method == 'POST':
        string_seq = request.form.get('quote1')
        ai_quote1 = api.get_ai_quote(string_seq)
        return render_template('home.html', quote_a = ai_quote1)
    return render_template('home.html')


# User Login and authentication
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['name']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            #return render_template('home.html')
            return redirect(url_for("home"))
        except:
            unsuccessful = 'Please check your credentials'
            return render_template('login.html', umessage=unsuccessful)
    return render_template('login.html')


# Create account page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['name']
        password = request.form['password']
        auth.create_user_with_email_and_password(email, password)
        return render_template('home.html')
    return render_template('signup.html')


# Submit a quote page. Only submits a quote if a user is currenly logged in and quote is not empty
@app.route('/upload', methods = ['GET', 'POST'])
def upload():
    if request.method == 'POST':
        try:
            user_quote = request.form['userQuote']
            # Check to see if user is logged in and quote is not empty.
            # If condiiton passes then add quote to db and display success message.
            if (user_quote.strip() != "" and auth.current_user != None):
                successful = 'Successfully submitted your {0} quote'.format(user_quote)
                api.add_user_quote(auth.current_user['email'], user_quote)
                return render_template('submit_quote.html', umessage=successful)
            elif (auth.current_user == None):
                unsuccessful = 'You need to be logged in to submit quote'
                return render_template('submit_quote.html', umessage=unsuccessful)
            else:
                return render_template('submit_quote.html', umessage="Can't submit empty quote value")
        except:
            unsuccessful = 'Unable to submit quote'
            return render_template('submit_quote.html', umessage=unsuccessful)
    return render_template('submit_quote.html')


# Generate quoute page
@app.route('/generate_quote', methods=['GET', 'POST'])  # generate quote page
def generate_quote():
    if request.method == 'POST':
        string_seq = request.form.get('quote1')
        ai_quote1 = api.get_ai_quote(string_seq)
        return render_template('generate_quote.html', quote_a = ai_quote1)
    return render_template('generate_quote.html')


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r




# app.run() deploys the website
if __name__ == "__main__":
    app.run(debug=True)
    # disabling while playing with container for FLASK application
    # app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
