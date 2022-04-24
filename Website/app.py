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
def demo():
    return render_template('demo.html')


# User Login and authentication
@app.route('/demo_login', methods=['GET', 'POST'])
def demo_login():
    if (request.method == 'POST'):
        email = request.form['name']
        password = request.form['password']
        try:
            auth.sign_in_with_email_and_password(email, password)
            # user_id = auth.get_account_info(user['idToken'])
            # session['usr'] = user_id
            return render_template('demo.html')
        except:
            unsuccessful = 'Please check your credentials'
            return render_template('demo_login.html', umessage=unsuccessful)
    return render_template('demo_login.html')


# Create account page
@app.route('/demo_signup', methods=['GET', 'POST'])
def demo_signup():
    if (request.method == 'POST'):
        email = request.form['name']
        password = request.form['password']
        auth.create_user_with_email_and_password(email, password)
        return render_template('demo.html')
    return render_template('demo_signup.html')


@app.route('/demo_upload')  # upload page
def demo_upload():
    return render_template('demo_upload_file.html')


@app.route('/demo_quote')  # generate quote page
def demo_quote():
    return render_template('demo_quote.html')


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
    app.run()
