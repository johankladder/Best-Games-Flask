from services.database_service import db


class Score(db.Model):
    id = db.Column(db.INT, primary_key=True)
    score = db.Column(db.INT)
    user_id = db.Column(db.INT, db.ForeignKey('user.id'))
    game_id = db.Column(db.INT, db.ForeignKey('game.id'))

    def __init__(self, score, uid, gid):
        self.score = score
        self.user_id = uid
        self.game_id = gid
