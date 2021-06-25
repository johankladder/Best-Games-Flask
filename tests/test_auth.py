from flask import json
from models.user import User
from models.block_list_token import BlockListToken
from conftest import get_authorised_headers



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


def test_is_authenticated_when_authenticated(client, database):
    rv = client.get("/authenticated", headers=get_authorised_headers())
    assert rv.status_code == 200


def test_is_authenticated_when_not_authenticated(client, database):
    rv = client.get("/authenticated")
    assert rv.status_code == 401


def test_is_authenticated_when_in_blocklist(client, database):
    authorization_headers = get_authorised_headers()
    client.post("/logout", headers=authorization_headers)
    rv = client.get("/authenticated", headers=authorization_headers)
    assert rv.status_code == 401


def test_logout(client, database):
    assert database.session.query(BlockListToken).count() is 0
    authorization_headers = get_authorised_headers()
    rv = client.post("/logout", headers=authorization_headers)
    assert rv.status_code == 200
    assert database.session.query(BlockListToken).count() is 1


def __create_user(username, password, database):
    user = User(username=username, password=password)
    database.session.add(user)
    database.session.commit()
