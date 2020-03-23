from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from libraryapp.config import Config
import logging

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s : %(levelname)s : %(message)s'
)

from libraryapp import routes
