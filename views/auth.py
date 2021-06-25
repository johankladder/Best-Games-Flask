from http.client import BAD_REQUEST
from flask import Blueprint, request, abort
from models.user import User, db
from flask_jwt_extended import create_access_token

from views.schemas.login_schema import LoginSchema

auth = Blueprint('auth', __name__)

login_schema = LoginSchema()


@auth.route('/login', methods=["POST"])
def login():
    data = request.get_json(silent=True)
    print(data)
    errors = login_schema.validate(data)
    if errors:
        abort(BAD_REQUEST, str(errors))

    username = data['username']
    password = data['password']

    user = __get_authenticated_user(username, password)
    if user is not None:
        return dict(
            id=user.id,
            token=create_access_token(identity=user.id)
        )
    abort(BAD_REQUEST, "Given credentials are not correct")


def __get_authenticated_user(username, password):
    user = db.session.query(User).filter_by(username=username).first()
    if user is not None:
        if user.password == password:
            return user
    return None
