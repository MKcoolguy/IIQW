import pyrebase
from flask import render_template, request, redirect, session
from app import app
import os

config = {
    "apiKey": "AIzaSyDW6j3T5zqNfpRHQrYZXk12hICYbzZzoxk",
    "authDomain": "iiqw-2ab5f.firebaseapp.com",
    "databaseURL": "https://iiqw-2ab5f-default-rtdb.firebaseio.com/",  # NEED # TODO: add databaseURL
    "projectId": "iiqw-2ab5f",
    "storageBucket": "iiqw-2ab5f.appspot.com",
    "messagingSenderId": "260325577865",
    "appId": "1:260325577865:web:a1969fa00e43030955e258"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


# @app.route('/')
@app.route('/', methods=['GET', 'POST'])
def demo():
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
            return render_template('index.html', umessage=unsuccessful)
    return render_template('index.html')


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        email = request.form['name']
        password = request.form['password']
        auth.create_user_with_email_and_password(email, password)
        return render_template('index.html')
    return render_template('create_account.html')


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['name']
        auth.send_password_reset_email(email)
        return render_template('index.html')
    return render_template('forgot_password.html')


@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


if __name__ == '__main__':  # method to run the application on a localhost
    app.run()
