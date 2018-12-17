import os
import credentials


BASEDIR = os.path.abspath(os.path.dirname(__file__))

DATABASE = credentials.DATABASE

WTF_CSRF_ENABLED = True

SECRET_KEY = credentials.SECRET_KEY

DATABASE_PATH = os.path.join(BASEDIR, DATABASE)

SQLALCHEMY_DATABASE_URI = 'sqlite:///'+DATABASE_PATH