
from engine.app import db
from engine.app.models import group_association


class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    user = db.relationship('User', secondary=group_association, back_populates='group')

    def __repr__(self):
        return '<Group %r' % self.user

    @property
    def serialized(self):
        return {
            'id': self.id,
            'name': self.name,
            'users': [
                {
                    'id': user.id,
                    'name': user.name,
                }
                for user in self.user
            ]
        }