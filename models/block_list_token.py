from services.database_service import db


class BlockListToken(db.Model):
    id = db.Column(db.INT, primary_key=True)
    token = db.Column(db.String(100))

    def __init__(self, token):
        self.token = token
