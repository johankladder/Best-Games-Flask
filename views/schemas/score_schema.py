from marshmallow import Schema, fields


class ScoreSchema(Schema):
    score = fields.Int(required=True)
