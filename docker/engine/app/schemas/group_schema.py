
from engine.app.schemas import *
from engine.app.models import Group


class GroupSchema(ma.Schema):
    class Meta:
        model = Group

    id = fields.Int(required=False)
    name = fields.Str()
    user = fields.List(fields.Integer())