from http.client import NOT_FOUND, BAD_REQUEST, CREATED

from flask import Blueprint, request, abort
from sqlalchemy.exc import IntegrityError

from models.user import User, db


from views.schemas.register_schema import RegisterSchema
from views.schemas.update_user_schema import UpdateUserSchema

user = Blueprint('user', __name__)


register_schema = RegisterSchema()
update_schema = UpdateUserSchema()


@user.route('/user/<uid>', methods=["get", "put"])
def get_user(uid):
    found_user = db.session.query(User).filter_by(id=uid).first()
    if found_user is None:
        abort(NOT_FOUND, "User is not found")

    if request.method == 'GET':
        return dict(
            id=found_user.id,
            username=found_user.username
        )

    if request.method == 'PUT':
        errors = update_schema.validate(request.form)
        if errors:
            abort(BAD_REQUEST, str(errors))
        else:
            found_user.username = request.form['username']
            found_user.password = request.form['password']
            db.session.commit()
            return 'User updated successfully!'


@user.route('/user/', methods=["post"])
def create_user():
    errors = register_schema.validate(request.form)
    if errors:
        abort(BAD_REQUEST, str(errors))

    username = request.form['username']
    password = request.form['password']

    created_user = User(username, password)
    try:
        db.session.add(created_user)
        db.session.commit()
        return 'User was created!', CREATED
    except IntegrityError:
        db.session.rollback()
        abort(BAD_REQUEST, "User already exists!")


