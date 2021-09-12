
import sys, uuid, os.path, json
from flask_testing import TestCase
from engine.app import app, db, User, Group


def create_user():
    user = User(name="name", password="password_hash", admin=False)
    db.session.add(user)
    db.session.commit()
    return user.id


class ProjectTest(TestCase):
    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_app(self):
        return app
