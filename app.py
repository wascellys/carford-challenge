from flask.json import jsonify
from flask_jwt_extended import JWTManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from core.views import auth, bp_cars, bp_owners, bp_users
from config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    db.init_app(app)
    with app.app_context():
        # db.drop_all()
        db.create_all()
    JWTManager(app)
    app.register_blueprint(auth)
    app.register_blueprint(bp_owners)
    app.register_blueprint(bp_cars)
    app.register_blueprint(bp_users)

    return app


app = create_app()
