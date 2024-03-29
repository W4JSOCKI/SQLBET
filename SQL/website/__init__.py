from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__,static_folder="static")
    app.config['SECRET_KEY'] = 'x'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .auth_admin import auth_admin
    from .portfel import portfel
    from .mecze import mecze
    from .opcje_admina import dod_admin
    from .kupon import kupony


    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(auth_admin, url_prefix='/')
    app.register_blueprint(portfel, url_prefix='/')
    app.register_blueprint(mecze, url_prefix='/')
    app.register_blueprint(dod_admin, url_prefix='/')
    app.register_blueprint(kupony, url_prefix='/')

    from .models import Uzytkownik,Kupon,Mecz,Zaklad,Kursy,Admin,Klient,Wplata,Wyplata,Portfel

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Uzytkownik.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')
