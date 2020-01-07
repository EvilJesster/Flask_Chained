import os

# configuration file for app


DEBUG = False

SECRET_KEY_REAL = os.urandom(64)
SECRET_KEY_FAKE = 'Ivan is really cool'

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
USE_SESSION_FOR_NEXT = True
