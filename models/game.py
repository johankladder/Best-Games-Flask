from models.shared import db


class Game(db.Model):
    id = db.Column(db.INT, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    url = db.Column(db.String(100), unique=True)

    def __init__(self, name, url):
        self.name = name
        self.url = url
