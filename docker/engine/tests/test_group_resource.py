
from engine.tests import *
from engine.app.models import Group


payload_post = {
    "name": "group",
    "user": []
}

payload_post_no_user = {
    "name": "group",
    "user": [1]
}

payload_put = {
    "name": "group1",
    "user": []
}


payload_put_no_name = {
    "user": []
}

payload_put_with_user = {
    "name": "group1",
    "user": []
}


class GroupResourceTest(ProjectTest):
    def setUp(self):
        super().setUp()

    def test_get_all(self):
        group_created = create_group()
        with app.test_client() as client:
            response = client.get('/api/groups', headers=headers)
            group = Group.query.filter_by(id=group_created).first()
            self.assertEqual(response.status_code, 200)
            expected = {"groups": [group.serialized]}
            self.assertEqual(response.json, expected)

    def test_get_not_found(self):
        with app.test_client() as client:
            response = client.get("/api/groups", headers=headers)
            self.assertEqual(response.status_code, 404)
            self.assertIn("Groups not found.", response.data.decode())

    def test_get_group(self):
        group_created = create_group()
        with app.test_client() as client:
            response = client.get(f'/api/groups/{group_created}', headers=headers)
            group = Group.query.filter_by(id=group_created).first()
            self.assertEqual(response.status_code, 200)
            expected = {"group": [group.serialized]}
            self.assertEqual(response.json, expected)

    def test_get_group_not_found(self):
        group_id = 1
        with app.test_client() as client:
            response = client.get(f'/api/groups/{group_id}', headers=headers)
            self.assertEqual(response.status_code, 404)
            self.assertIn(f"Group {group_id} not found.", response.data.decode())

    def test_post(self):
        with app.test_client() as client:
            response = client.post("/api/groups", json=payload_post, headers=headers)
            self.assertEqual(response.status_code, 201)
            group_name = payload_post.get("name")
            group = Group.query.filter_by(name=group_name).first()
            self.assertEqual(response.json, group.serialized)

    def test_post_no_data_provided(self):
        with app.test_client() as client:
            response = client.post("/api/groups", headers=headers) ## Sem JSON
            self.assertEqual(response.status_code, 400)
            self.assertIn("Bad Request", response.data.decode())

    def test_post_no_name(self):
        payload_no_name = {}
        with app.test_client() as client:
            response = client.post("/api/groups", json=payload_no_name, headers=headers)
            self.assertEqual(response.status_code, 400)
            self.assertIn("Name is required", response.data.decode())

    def test_post_no_user_found(self):
        with app.test_client() as client:
            response = client.post("/api/groups", json=payload_post_no_user, headers=headers)
            self.assertEqual(response.status_code, 404)
            user_id = payload_post_no_user.get("user")[0]
            self.assertIn(f"User {user_id} not found.", response.data.decode())

    def test_delete(self):
        group_created = create_group()
        with app.test_client() as client:
            response = client.delete(f"/api/groups/{group_created}", headers=headers)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {"status": True})

    def test_delete_not_found(self):
        group_id = 1
        with app.test_client() as client:
            response = client.delete(f"/api/groups/{group_id}", headers=headers)
            self.assertEqual(response.status_code, 404)
            self.assertIn("Group not found.", response.data.decode())

    def test_put(self):
        group_created = create_group()
        with app.test_client() as client:
            response = client.put(f"/api/groups/{group_created}", json=payload_put, headers=headers)
            self.assertEqual(response.status_code, 200)
            group = Group.query.filter_by(id=group_created).first()
            self.assertEqual(response.json, group.serialized)

    def test_put_no_data_provided(self):
        group_created = create_group()
        with app.test_client() as client:
            response = client.put(f"/api/groups/{group_created}", headers=headers) ## Sem JSON
            self.assertEqual(response.status_code, 400)
            self.assertIn("Bad Request", response.data.decode())

    def test_put_no_name(self):
        group_created = create_group()
        with app.test_client() as client:
            response = client.put(f"/api/groups/{group_created}", json=payload_put_no_name, headers=headers)
            self.assertEqual(response.status_code, 400)
            self.assertIn("Name is required", response.data.decode())

    def test_put_group_not_found(self):
        group_id = 1
        with app.test_client() as client:
            response = client.put(f"/api/groups/{group_id}", json=payload_put, headers=headers)
            self.assertEqual(response.status_code, 404)
            self.assertIn(f"Group {group_id} not found.", response.data.decode())

