import pyrebase
from flask import render_template, request, redirect, session, Flask
import os

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
@app.route("/")
def home():
    return render_template('home.html')


# User Login and authentication
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['name']
        password = request.form['password']
        try:
            auth.sign_in_with_email_and_password(email, password)
            # user_id = auth.get_account_info(user['idToken'])
            # session['usr'] = user_id
            return render_template('home.html')
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


@app.route('/upload')  # upload page
def upload():
    return render_template('submit_quote.html')


@app.route('/generate_quote')  # generate quote page
def generate_quote():
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
