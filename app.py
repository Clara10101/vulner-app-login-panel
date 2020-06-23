from flask import Flask, flash, redirect, render_template, \
     request, url_for, send_from_directory
import os
from sqlalchemy.orm import sessionmaker
from passlib.hash import sha256_crypt
from tabledef import *
from werkzeug.utils import secure_filename
from zipfile import ZipFile
engine = create_engine('sqlite:///tutorial.db', echo=True)

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#file upload configuration
UPLOAD_FOLDER = ''
#UPLOAD_FOLDER = '\\uploads'
#ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip'}
ALLOWED_EXTENSIONS = {'zip'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            zip_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(zip_file)

            # opening the zip file in READ mode
            with ZipFile(zip_file, 'r') as zip:
                # printing all the contents of the zip file
                zip.printdir()

                # extracting all the files
                print('Extracting all the files now...')
                zip.extractall()
                print('Done!')

            #filename_unzipped =

            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)