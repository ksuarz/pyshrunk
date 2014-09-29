import os
from flask import Flask

app = Flask(__name__)
app.debug = True
app.config.from_pyfile('../config.py')

from app import views, models
