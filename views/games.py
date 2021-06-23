from http.client import NOT_FOUND
from flask import Blueprint, abort
from flask_jwt_extended import jwt_required
from models.game import Game, db
import json

games = Blueprint('games', __name__)


@games.before_request
@jwt_required()
def before():
    return


@games.route('/games', methods=["get"])
def get_games():
    found_games = []
    for found_game in db.session.query(Game).all():
        found_games.append(__get_game_dict(found_game))

    return json.dumps(found_games)


@games.route('/games/<gid>', methods=["get"])
def game(gid):
    found_game = __get_game(gid=gid)
    if found_game is not None:
        return __get_game_dict(found_game)
    else:
        abort(NOT_FOUND, 'Game was not found!')


def __get_game(gid):
    return db.session.query(Game).filter_by(id=gid).first()


def __get_game_dict(found_game):
    return dict(
        id=found_game.id,
        name=found_game.name,
        url=found_game.url
    )




