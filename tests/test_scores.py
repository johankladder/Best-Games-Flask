from flask import json

from conftest import create_user, create_game, create_score, get_authorised_headers
from models.score import Score


def __create_score_with_game(gid, uid, score, database):
    return create_score(
        score=score,
        uid=uid,
        gid=gid,
        database=database
    )


class TestMyScores:

    def test_get_scores_invalid_user_id(self, client, database):
        rv = client.get('/myscores')
        assert rv.status_code == 401

    def test_get_scores_empty(self, client, database):
        rv = client.get('/myscores', headers=get_authorised_headers())
        assert rv.status_code == 200

        data = json.loads(rv.data)
        assert len(data) == 0

    def test_get_scores(self, client, database):
        user = create_user('johankladder', 'password', database)
        game = create_game('memory', 'www.memory.nl', database)
        score = create_score(1, user.id, game.id, database)

        rv = client.get('/myscores', headers=get_authorised_headers(user))
        assert rv.status_code == 200

        data = json.loads(rv.data)
        assert len(data) == 1
        assert data[0]['id'] == score.id
        assert data[0]['score'] == score.score

    def test_get_scores_multi_users(self, client, database):
        user_1 = create_user('johankladder', 'password', database)
        user_2 = create_user('johankladder2', 'password', database)
        game = create_game('memory', 'www.memory.nl', database)
        score_1 = create_score(1, user_1.id, game.id, database)
        create_score(1, user_2.id, game.id, database)

        rv = client.get('/myscores', headers=get_authorised_headers(user_1))
        assert rv.status_code == 200

        data = json.loads(rv.data)
        assert len(data) == 1
        assert data[0]['id'] == score_1.id
        assert data[0]['score'] == score_1.score

    def test_get_top_scores_invalid_game(self, client, database):
        rv = client.get('/topscores/1', headers=get_authorised_headers())
        assert rv.status_code == 404

    def test_get_top_scores_empty_scores(self, client, database):
        game = create_game('memory', 'www.memory.nl', database)
        rv = client.get('/topscores/' + str(game.id), headers=get_authorised_headers())
        assert rv.status_code == 200

        data = json.loads(rv.data)
        assert len(data) == 0

    def test_get_top_scores_scores_less_then_10(self, client, database):
        game = create_game('memory', 'www.memory.nl', database)
        user = create_user('johankladder', 'password', database)
        create_score(10, game.id, user.id, database)
        create_score(9, game.id, user.id, database)
        create_score(8, game.id, user.id, database)

        rv = client.get('/topscores/' + str(game.id), headers=get_authorised_headers(user))
        assert rv.status_code == 200

        data = json.loads(rv.data)
        assert len(data) == 3
        assert data[0]['score'] == 8
        assert data[1]['score'] == 9
        assert data[2]['score'] == 10

    def test_get_top_scores_scores_more_then_10(self, client, database):
        game = create_game('memory', 'www.memory.nl', database)
        user = create_user('johankladder', 'password', database)
        create_score(11, game.id, user.id, database)
        create_score(10, game.id, user.id, database)
        create_score(9, game.id, user.id, database)
        create_score(7, game.id, user.id, database)
        create_score(6, game.id, user.id, database)
        create_score(5, game.id, user.id, database)
        create_score(4, game.id, user.id, database)
        create_score(3, game.id, user.id, database)
        create_score(2, game.id, user.id, database)
        create_score(1, game.id, user.id, database)

        rv = client.get('/topscores/' + str(game.id), headers=get_authorised_headers(user))
        assert rv.status_code == 200

        data = json.loads(rv.data)
        assert len(data) == 10
        assert data[0]['score'] == 1
        assert data[1]['score'] == 2
        assert data[2]['score'] == 3

    def test_add_score_invalid_game(self, client, database):
        rv = client.post('/myscores/12', headers=get_authorised_headers())
        assert rv.status_code == 404

    def test_add_score_invalid_params(self, client, database):
        game = create_game('memory', 'www.memory.nl', database)
        rv = client.post('/myscores/' + str(game.id), headers=get_authorised_headers())
        assert rv.status_code == 400

    def test_add_score_happy_flow(self, client, database):
        assert database.session.query(Score).count() == 0
        game = create_game('memory', 'www.memory.nl', database)
        rv = client.post('/myscores/' + str(game.id), json=dict(
            score=1
        ), headers=get_authorised_headers())
        assert rv.status_code == 201
        assert database.session.query(Score).count() == 1