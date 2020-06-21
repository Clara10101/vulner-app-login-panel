from flask import Flask
from flask_httpauth import HTTPDigestAuth

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
auth = HTTPDigestAuth()

users = {
    "admin": "admin",
    "tester01": "qwerty",
    "tester02": "a3b2c1"
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route('/')
@auth.login_required
def index():
    return "Hello, %s!" % auth.username()