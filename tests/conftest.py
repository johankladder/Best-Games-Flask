import pytest
from flask_jwt_extended import create_access_token

from app import create_app, db
from models.user import User
from models.game import Game
from models.score import Score


@pytest.fixture
def app():
    app = create_app(is_test=True)
    yield app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture
def database(app):
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()


def create_user(username, password, database):
    user = User(username=username, password=password)
    database.session.add(user)
    database.session.commit()
    return user


def create_game(name, url, database):
    game = Game(name=name, url=url)
    database.session.add(game)
    database.session.commit()
    return game


def create_score(score, uid, gid, database):
    score = Score(score=score,uid=uid, gid=gid)
    database.session.add(score)
    database.session.commit()
    return score


def get_authorised_headers(user: User = None):
    if user is None:
        user = create_user('johankladder', 'password', db)
    access_token = create_access_token(identity=user.id)
    authorization = 'Bearer ' + access_token
    return {
        'Authorization': authorization
    }