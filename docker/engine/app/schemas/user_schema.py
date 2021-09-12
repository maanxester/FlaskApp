
from engine.app.schemas import *
from engine.app.models import User


class UserSchema(ma.Schema):
    class Meta:
        model = User

    id = fields.Int(required=False)
    name = fields.Str()
    password = fields.Str()
    admin = fields.Boolean()
    group = fields.List(fields.Integer())
