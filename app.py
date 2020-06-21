from flask import Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("admin"),
    "tester01": generate_password_hash("qwerty"),
    "tester02": generate_password_hash("a3b2c1")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/')
@auth.login_required
def index():
    return "Hello, %s!" % auth.current_user()