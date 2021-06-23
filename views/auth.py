from http.client import BAD_REQUEST
from flask import Blueprint, request, abort
from models.user import User, db

from views.schemas.login_schema import LoginSchema

auth = Blueprint('auth', __name__)

login_schema = LoginSchema()


@auth.route('/login', methods=["POST"])
def login():
    errors = login_schema.validate(request.form)
    if errors:
        abort(BAD_REQUEST, str(errors))

    username = request.form['username']
    password = request.form['password']

    user = __get_authenticated_user(username, password)
    if user is not None:
        return dict(token="jwt-token", id=user.id)

    abort(BAD_REQUEST, "Given credentials are not correct")


def __get_authenticated_user(username, password):
    user = db.session.query(User).filter_by(username=username).one()
    if user is not None:
        if user.password == password:
            return user
    return None
