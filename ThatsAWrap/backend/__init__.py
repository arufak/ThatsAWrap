# makes the website folder a python package

from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_Name = "database.db"

app = Flask(__name__) 

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secretkeyyyyy'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_Name}' # database location 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app) 

    from .views import views 
    from .auth import auth 

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/') 

    from .models import User

    with app.app_context():
        create_database(app) 

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' 
    login_manager.init_app(app) 

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id)) # telling flask how to load a user

    return app 

def create_database(app):
    if not path.exists('website/' + DB_Name):
        db.create_all(app=app)
        print('Created Database!')

