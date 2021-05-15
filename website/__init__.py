from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'adxasfdbvnbhn'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    from .view import view
    from .auth import auth

    app.register_blueprint(view, url_prefix='')
    app.register_blueprint(auth, url_prefix='')

    from .model import Room, Player, Message

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.create_room'
    login_manager.init_app(app=app)

    @login_manager.user_loader
    def load_user(id):
        return Player.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Database has been created!!')
