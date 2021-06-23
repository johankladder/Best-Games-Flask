from flask import json

from conftest import create_game


class TestGames:

    def test_get_games_empty(self, client, database):
        rv = client.get("/games")
        assert rv.status_code == 200

    def test_get_games(self, client, database):
        create_game(name='Memory', url='https://www.memory.nl', database=database),
        create_game(name='TicTacToe', url='https://www.tictactoe.nl', database=database),

        rv = client.get("/games")
        assert rv.status_code == 200

        data = json.loads(rv.data)
        assert len(data) == 2

    def test_get_game_not_existing(self, client, database):
        rv = client.get("/games/1")
        assert rv.status_code == 404

    def test_get_game(self, client, database):
        game = create_game(name='Memory', url='https://www.google.nl', database=database)
        rv = client.get("/games/" + str(game.id))
        assert rv.status_code == 200

        data = json.loads(rv.data)
        assert data['id'] == game.id
        assert data['name'] == game.name
        assert data['url'] == game.url
