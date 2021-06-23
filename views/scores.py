from http.client import NOT_FOUND
from flask import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.shared import db
from models.user import User, get_by_jwt_identifier
from models.score import Score
from models.game import Game
import json


scores = Blueprint('my_scores', __name__)


@scores.before_request
@jwt_required()
def before():
    return


@scores.route('/myscores', methods=["get"])
def get_scores():
    found_user = get_by_jwt_identifier(get_jwt_identity())
    if found_user is not None:
        found_scores = []

        for found_score in __get_scores(found_user):
            found_scores.append(__get_score_dict(found_score))

        return json.dumps(found_scores)
    else:
        abort(NOT_FOUND, 'User was not found!')


@scores.route('/topscores/<gid>', methods=["get"])
def get_top_scores(gid):
    found_game = __get_game(gid)
    if found_game is not None:
        found_scores = []
        for found_score in __get_top_scores(found_game):
            found_scores.append(__get_score_dict(found_score))
        return json.dumps(found_scores)
    else:
        abort(NOT_FOUND, 'Game was not found!')


def __get_game(gid):
    return db.session.query(Game).filter_by(id=gid).first()


def __get_scores(user: User):
    return db.session.query(Score).filter_by(user_id=user.id).all()


def __get_top_scores(game: Game):
    return db.session.query(Score)\
        .filter_by(game_id=game.id)\
        .order_by(Score.score.asc())\
        .limit(10)\
        .all()


def __get_score_dict(score: Score):
    return dict(
        id=score.id,
        score=score.score
    )
