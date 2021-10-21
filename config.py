import os
from os.path import abspath, dirname

from dotenv import load_dotenv

BASEDIR = abspath(dirname(__file__))

load_dotenv()
TESTING = os.getenv('TESTING')
