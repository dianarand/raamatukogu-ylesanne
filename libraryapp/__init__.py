from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from libraryapp.config import Config

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message = 'Logi sisse, et näha seda lehte'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    from libraryapp.main.routes import main
    from libraryapp.books.routes import books
    from libraryapp.lenders.routes import lenders
    app.register_blueprint(main)
    app.register_blueprint(books)
    app.register_blueprint(lenders)

    return app
