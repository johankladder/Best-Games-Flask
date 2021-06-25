from services.database_service import db


def get_by_jwt_identifier(identifier):
    return db.session.query(User).filter_by(id=identifier).first()


class User(db.Model):
    id = db.Column(db.INT, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username
        self.password = password
