
from engine.tests import *


payload_post = {
    "name": "unittest",
    "password": "unittest",
    "admin": False,
    "group": []
}

payload_post_no_group = {
    "name": "unittest",
    "password": "unittest",
    "admin": False,
    "group": [1]
}

payload_post_no_name = {
    "password": "unittest",
    "admin": False,
    "group": []
}

payload_put = {
    "name": "name",
    "password": "password_hash1",
    "admin": False,
    "group": []
}

payload_put_no_name = {
    "password": "password_hash",
    "admin": False,
    "group": []
}

payload_put_no_group = {
    "name": "name",
    "password": "password_hash",
    "admin": False,
    "group": [1]
}

payload_post_no_password = {
    "name": "unittest",
    "admin": False,
    "group": []
}


class UserResourceTest(ProjectTest):
    def setUp(self):
        super().setUp()

    def test_get_all(self):
        user_created = create_user()
        with app.test_client() as client:
            response = client.get('/users')
            self.assertEqual(response.status_code, 200)
            user = User.query.filter_by(id=user_created).first()
            expected = {"users": [user.serialized]}
            self.assertEqual(response.json, expected)

    def test_get_all_not_found(self):
        with app.test_client() as client:
            response = client.get('/users')
            self.assertEqual(response.status_code, 404)
            self.assertIn("No users found.", response.data.decode())

    def test_get_user(self):
        user_created = create_user()
        with app.test_client() as client:
            response = client.get(f'/users/{user_created}')
            self.assertEqual(response.status_code, 200)
            user = User.query.filter_by(id=user_created).first()
            expected = {"users": [user.serialized]}
            self.assertEqual(response.json, expected)

    def test_get_user_not_found(self):
        user_id = 1
        with app.test_client() as client:
            response = client.get(f'/users/{user_id}')
            self.assertEqual(response.status_code, 404)
            self.assertIn(f"User {user_id} not found.", response.data.decode())

    def test_post(self):
        with app.test_client() as client:
            response = client.post("/users", json=payload_post)
            self.assertEqual(response.status_code, 201)
            user = User.query.filter_by(name=payload_post["name"]).first()
            self.assertIsNotNone(user)
            self.assertEqual(response.json, user.serialized)

    def test_post_no_data_provided(self):
        with app.test_client() as client:
            response = client.post("/users") ## Sem JSON
            self.assertEqual(response.status_code, 400)
            self.assertIn("No data provided.", response.data.decode())

    def test_post_no_name(self):
        with app.test_client() as client:
            response = client.post("/users", json=payload_post_no_name)
            self.assertEqual(response.status_code, 400)
            self.assertIn("Name is required", response.data.decode())

    def test_post_no_password(self):
        with app.test_client() as client:
            response = client.post("/users", json=payload_post_no_password)
            self.assertEqual(response.status_code, 400)
            self.assertIn("Password is required", response.data.decode())

    def test_post_group_not_found(self):
        with app.test_client() as client:
            response = client.post('/users', json=payload_post_no_group)
            self.assertEqual(response.status_code, 404)
            no_group = payload_post_no_group["group"][0]
            self.assertIn(f"Group {no_group} not found.", response.data.decode())

    def test_delete(self):
        user_created = create_user()
        with app.test_client() as client:
            response = client.delete(f'/users/{user_created}')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {"status": True})

    def test_delete_user_not_found(self):
        user_id = 1
        with app.test_client() as client:
            response = client.delete(f'/users/{user_id}')
            self.assertEqual(response.status_code, 404)
            self.assertIn(f"User {user_id} not found.", response.data.decode())

    def test_put(self):
        user_created = create_user()
        with app.test_client() as client:
            response = client.put(f"/users/{user_created}", json=payload_put)
            self.assertEqual(response.status_code, 200)
            user = User.query.filter_by(id=user_created).first()
            self.assertEqual(response.json, user.serialized)

    def test_put_no_data_provided(self):
        user_created = create_user()
        with app.test_client() as client:
            response = client.put(f"/users/{user_created}") ## Sem JSON
            self.assertEqual(response.status_code, 400)
            self.assertIn("No data provided.", response.data.decode())

    def test_put_not_name(self):
        user_created = create_user()
        with app.test_client() as client:
            response = client.put(f"/users/{user_created}", json=payload_put_no_name)
            self.assertEqual(response.status_code, 400)
            self.assertIn("Required to enter valid name", response.data.decode())

    def test_put_not_user(self):
        user_id = 1
        with app.test_client() as client:
            response = client.put(f"/users/{user_id}", json=payload_put)
            self.assertEqual(response.status_code, 404)
            self.assertIn(f"User {user_id} not found.", response.data.decode())

    def test_put_no_group_found(self):
        user_created = create_user()
        with app.test_client() as client:
            response = client.put(f"/users/{user_created}", json=payload_put_no_group)
            group_id = payload_post_no_group["group"][0]
            self.assertEqual(response.status_code, 404)
            self.assertIn(f"Group {group_id} not found.", response.data.decode())
