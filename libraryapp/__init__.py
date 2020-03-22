from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd46de97837b274867df6ac9d2861bb9b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'main.login'
login_manager.login_message = 'Logi sisse, et näha seda lehte'

from libraryapp.main.routes import main
from libraryapp.books.routes import books
from libraryapp.lenders.routes import lenders

app.register_blueprint(main)
app.register_blueprint(books)
app.register_blueprint(lenders)
