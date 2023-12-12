from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from itsdangerous import URLSafeTimedSerializer

from os import environ

if environ.get("ENVIRONMENT")=="vercel":
    postgres_user = environ["POSTGRES_USER"]
    postgres_password = environ["POSTGRES_PASSWORD"]
    postgres_host = environ["POSTGRES_HOST"]
    postgres_database = environ["POSTGRES_DATABASE"]
else:
    postgres_user = "postgres"
    postgres_password = "root"
    postgres_host = "localhost"
    postgres_database = "birdinv5"

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.cfg")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}/{postgres_database}"
    db.init_app(app)

    app.mail_verify_serializer = URLSafeTimedSerializer(app.config["MAIL_SECRET_KEY"])

    from .views import views
    from .auth import auth
    from .api import api
    from .admin import admin
    from .store import store

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(api, url_prefix="/")
    app.register_blueprint(admin, url_prefix="/")
    app.register_blueprint(store, url_prefix="/")

    from .models import UserSpecies, UnverifiedUser, User, Species, NicknameHistory
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

