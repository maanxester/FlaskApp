
from engine.tests import *
from engine.app.models import Group


class GroupResourceTest(ProjectTest):
    def setUp(self):
        super().setUp()

    def test_get_all(self):
        group_created = create_group()
        with app.test_client() as client:
            response = client.get('/groups')
            group = Group.query.filter_by(id=group_created).first()
            self.assertEqual(response.status_code, 200)
            expected = {"groups": [group.serialized]}
            self.assertEqual(response.json, expected)