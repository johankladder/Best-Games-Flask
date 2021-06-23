from flask import json

from conftest import create_user
from models.user import User


class TestUser:

    def test_get_user_with_invalid_id(self, client, database):
        rv = client.get("/user/1")
        assert rv.status_code == 404

    def test_get_user_with_valid_id(self, client, database):
        user = create_user(username='johankladder', password='password', database=database)
        rv = client.get("/user/" + str(user.id))
        assert rv.status_code == 200

        data = json.loads(rv.data)
        assert data['id'] == user.id
        assert data['username'] == user.username

    def test_create_user_with_missing_values(self, client, database):
        rv = client.post("/user/", data=dict())
        assert rv.status_code == 400

        rv = client.post("/user/", data=dict(
            username='johankladder'
        ))
        assert rv.status_code == 400

        rv = client.post("/user/", data=dict(
            password='johankladder'
        ))
        assert rv.status_code == 400

    def test_create_user(self, client, database):
        rv = client.post("/user/", data=dict(
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

        rv = client.post("/user/", data=dict(
            username='johankladder',
            password='password'
        ))

        assert rv.status_code == 400

    def test_update_not_existing_user(self, client, database):
        rv = client.put("/user/1", data=dict(
            username='johankladder',
            password='updated-password'
        ))

        assert rv.status_code == 404

    def test_update_existing_user_missing_fields(self, client, database):
        user = create_user(username='johankladder', password='password', database=database)
        rv = client.put("/user/" + str(user.id), data=dict(
            username='johankladder',
        ))

        assert rv.status_code == 400

    def test_update_existing_user(self, client, database):
        user = create_user(username='johankladder', password='password', database=database)
        rv = client.put("/user/" + str(user.id), data=dict(
            username='updated-johankladder',
            password='updated-password'
        ))

        assert rv.status_code == 200

        user = database.session.query(User).filter_by(username='updated-johankladder', password='updated-password').first()
        assert user is not None



