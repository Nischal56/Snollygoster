from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = "snollygoster"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.yt_api_dev'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    app.config['TEMPLATES_AUTO_RELOAD'] = True



    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import Users

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    db.init_app(app)


    # CARE FROM HERE DOWN
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .dashboard import dashboard as dashboard_blueprint
    app.register_blueprint(dashboard_blueprint)

    return app