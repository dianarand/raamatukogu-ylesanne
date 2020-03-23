from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from libraryapp.config import Config
import logging

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

logging.basicConfig(level=logging.INFO)

from libraryapp import routes
