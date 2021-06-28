from http.client import NOT_FOUND, BAD_REQUEST, CREATED
from flask import Blueprint, abort, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.database_service import db
from models.user import User, get_by_jwt_identifier
from models.score import Score
from models.game import Game
import json
from views.schemas.score_schema import ScoreSchema

scores = Blueprint('my_scores', __name__)

score_schema = ScoreSchema()


@scores.route('/myscores', methods=["get"])
@jwt_required()
def get_scores():
    found_user = get_by_jwt_identifier(get_jwt_identity())
    if found_user is not None:
        found_scores = []

        for found_score in __get_scores(found_user):
            found_scores.append(__get_score_dict(found_score))

        return json.dumps(found_scores)
    else:
        abort(NOT_FOUND, 'User was not found!')


@scores.route('/myscores/<gid>', methods=["post"])
@jwt_required()
def add_score(gid):
    found_user = get_by_jwt_identifier(get_jwt_identity())
    found_game = __get_game(gid)
    data = request.get_json(silent=True)
    errors = score_schema.validate(data)

    if errors:
        abort(BAD_REQUEST, str(errors))

    if found_game is not None and found_user is not None:
        new_score = Score(
            score = data['score'],
            uid = found_user.id,
            gid = found_game.id
        )
        db.session.add(new_score)
        db.session.commit()
        return "Score was created!", CREATED
    else:
        abort(NOT_FOUND, 'User was not found!')


@scores.route('/topscores/<gid>', methods=["get"])
@jwt_required()
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
        user_id=score.user_id,
        score=score.score,
        username=score.user.username
    )
