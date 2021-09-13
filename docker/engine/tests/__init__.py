
import sys, uuid, os.path, json
from flask_testing import TestCase
from engine.app import app, db, User, Group


def create_user():
    user = User(name="name", password="password_hash", admin=False)
    db.session.add(user)
    db.session.commit()
    return user.id


def create_group():
    group = Group(name="name")
    db.session.add(group)
    db.session.commit()
    return group.id


headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic YWRtaW46YWRtaW4='
}


class ProjectTest(TestCase):
    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_app(self):
        return app
