import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *
from passlib.hash import sha256_crypt

engine = create_engine('sqlite:///tutorial.db', echo=True)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

user = User("admin",sha256_crypt.hash("admin"))
session.add(user)

user = User("tester01",sha256_crypt.hash("qwerty"))
session.add(user)

user = User("tester02",sha256_crypt.hash("a3b2c1"))
session.add(user)

# commit the record the database
session.commit()