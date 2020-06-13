from flask import Flask, flash, redirect, render_template, \
     request, url_for
import os
from sqlalchemy.orm import sessionmaker
from passlib.hash import sha256_crypt
from tabledef import *
engine = create_engine('sqlite:///tutorial.db', echo=True)

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':

        POST_USERNAME = str(request.form['username'])
        POST_PASSWORD = str(request.form['password'])

        Session = sessionmaker(bind=engine)
        s = Session()
        query_user = s.query(User).filter(User.username.in_([POST_USERNAME]))

        result_user = query_user.first()

        if result_user:

            hash = result_user.password

            if sha256_crypt.verify(POST_PASSWORD, hash):
                print("Zalogowany")
                flash('You were successfully logged in')
                return redirect(url_for('index'))
        else:
            sha256_crypt.verify(POST_PASSWORD, "$5$rounds=535000$jp1pVmu1RFmA4c1U$lOitOIXcKjimfwceyqgLHFK1kKfsVGNLb/s3U2pdeKC")
        error = 'Invalid credentials'

    return render_template('login.html', error=error)

@app.route('/test')
def test():

    POST_USERNAME = "admin"
    POST_PASSWORD = "admin"

    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        return "Object found"
    else:
        return "Object not found " + POST_USERNAME + " " + POST_PASSWORD