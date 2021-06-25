from flask import json
from models.user import User


def test_login_missing_credentials(client):
    rv = client.post("/login")
    assert 400 == rv.status_code


def test_login_wrong_credentials(client, database):
    __create_user(username='johankladder', password='password', database=database)

    rv = client.post("/login", json=dict(
        username='johankladder',
        password='wrong-password'
    ))
    assert rv.status_code == 400


def test_login_correct_credentials(client, database):
    __create_user(username='johankladder', password='password', database=database)

    rv = client.post("/login", json=dict(
        username='johankladder',
        password='password'
    ))
    assert rv.status_code == 200

    data = json.loads(rv.data)
    assert data['token'] is not None
    assert data['id'] is not None


def __create_user(username, password, database):
    user = User(username=username, password=password)
    database.session.add(user)
    database.session.commit()
