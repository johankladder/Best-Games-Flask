from flask import json

from conftest import create_user, get_authorised_headers
from models.user import User


class TestUser:

    def test_get_user_with_invalid_id(self, client, database):
        rv = client.get("/user/2", headers=get_authorised_headers())
        assert rv.status_code == 404

    def test_get_user_with_valid_id(self, client, database):
        user = create_user(username='johankladder-test', password='password', database=database)
        rv = client.get("/user/" + str(user.id), headers=get_authorised_headers())
        assert rv.status_code == 200

        data = json.loads(rv.data)
        assert data['id'] == user.id
        assert data['username'] == user.username

    def test_create_user_with_missing_values(self, client, database):
        rv = client.post("/user", json=dict())
        assert rv.status_code == 400

        rv = client.post("/user", json=dict(
            username='johankladder'
        ))
        assert rv.status_code == 400

        rv = client.post("/user", json=dict(
            password='johankladder'
        ))
        assert rv.status_code == 400

    def test_create_user(self, client, database):
        rv = client.post("/user", json=dict(
            username='johankladder',
            password='password'
        ))
        assert rv.status_code == 201

        user = database.session.query(User).filter_by(username='johankladder').first()
        assert user is not None

    def test_create_duplicated_user(self, client, database):
        user = User('johankladder','password')
        database.session.add(user)
        database.session.commit()

        rv = client.post("/user", json=dict(
            username='johankladder',
            password='password'
        ))

        assert rv.status_code == 400

    def test_update_not_authorized(self, client, database):
        rv = client.put("/user", json=dict(
            username='johankladder',
            password='updated-password'
        ))
        assert rv.status_code == 401

    def test_update_existing_user_missing_fields(self, client, database):
        user = create_user(username='johankladder', password='password', database=database)
        rv = client.put("/user", json=dict(
            username='johankladder',
        ), headers=get_authorised_headers(user))
        assert rv.status_code == 400

    def test_update_existing_user(self, client, database):
        user = create_user(username='johankladder', password='password', database=database)
        rv = client.put("/user", json=dict(
            username='updated-johankladder',
            password='updated-password'
        ), headers=get_authorised_headers(user))

        assert rv.status_code == 200

        user = database.session.query(User).filter_by(
            username='updated-johankladder',
            password='updated-password'
        ).first()

        assert user is not None



