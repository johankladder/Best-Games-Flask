from flask import Flask
from flask_cors import CORS
from views.auth import auth
from views.user import user
from views.games import games
from views.scores import scores
from flask_jwt_extended import JWTManager
from models.shared import db

import os


def create_app(isTest = False):

    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    jwt = JWTManager(app)
    app.register_blueprint(auth)
    app.register_blueprint(user)
    app.register_blueprint(games)
    app.register_blueprint(scores)
    basedir = os.path.abspath(os.path.dirname(__file__))
    database = 'db.sqlite' if isTest is not True else 'db-test.sqlite'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, database)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'super-secret-jwt-key'
    db.init_app(app)
    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run()
