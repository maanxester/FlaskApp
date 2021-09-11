
from engine.app import db
from engine.app.models import group_association
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120)) ## HASH
    admin = db.Column(db.Boolean)
    group = db.relationship('Group', secondary=group_association, back_populates='user')

    def __repr__(self):
        return '<User %r' % self.name

    @property
    def serialized(self):
        return {
            'id': self.id,
            'name': self.name,
            'admin': self.admin,
            'groups': [
                {
                    'id': group.id,
                    'name': group.name,
                }
                for group in self.group
            ]
        }

    @property
    def password(self):
        raise AttributeError('Hidden Password')

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    def verify_password(self, value):
        return check_password_hash(self.password_hash, value)
