from http.client import NOT_FOUND, BAD_REQUEST, CREATED

from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import get_jwt_identity

from models.user import User, db, get_by_jwt_identifier

from views.schemas.register_schema import RegisterSchema
from views.schemas.update_user_schema import UpdateUserSchema

user = Blueprint('user', __name__)

register_schema = RegisterSchema()
update_schema = UpdateUserSchema()


@user.route('/user/<uid>', methods=["get"])
@jwt_required()
def get_user(uid):
    found_user = db.session.query(User).filter_by(id=uid).first()
    if found_user is None:
        abort(NOT_FOUND, "User is not found")
    else:
        return dict(
            id=found_user.id,
            username=found_user.username
        )


@user.route('/user', methods=["POST"])
def create_user():
    data = request.get_json(silent=True)
    errors = register_schema.validate(data)
    if errors:
        abort(BAD_REQUEST, str(errors))

    username = data['username']
    password = data['password']

    created_user = User(username, password)
    try:
        db.session.add(created_user)
        db.session.commit()
        return 'User was created!', CREATED
    except IntegrityError:
        db.session.rollback()
        abort(BAD_REQUEST, "User already exists!")


@user.route('/user', methods=["put"])
@jwt_required()
def update_user():
    found_user = get_by_jwt_identifier(get_jwt_identity())
    data = request.get_json(silent=True)
    errors = update_schema.validate(data)
    if errors or found_user is None:
        abort(BAD_REQUEST, str(errors))
    else:
        found_user.username = data['username']
        found_user.password = data['password']
        db.session.commit()
        return 'User updated successfully!'



