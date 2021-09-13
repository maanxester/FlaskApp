
from engine.app import app, db, ADMIN_USERNAME, ADMIN_PASSWORD
from flask import jsonify, request, abort
from engine.app.resources.api import api
from engine.app.models.users import User
from engine.app.models.groups import Group
from engine.app.schemas import ValidationError, user_schema
from functools import wraps


def auth(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.authorization
        name_entered = data.get("username")
        password_entered = data.get("password")
        if name_entered == ADMIN_USERNAME and password_entered == ADMIN_PASSWORD:
            return f(*args, **kwargs)
        user = User.query.filter_by(name=name_entered).first()
        if user is None or not user.verify_password(password_entered) or user.admin is False:
            abort(401, 'User or password is incorrect.')
        return f(*args, **kwargs)
    return wrap


def validations(data):
    name = data.get("name")
    if not name:
        abort(400, "Name is required.")

    password = data.get("password")
    if not password:
        abort(400, "Password is required.")


@api.route('/users',  methods=['GET'])
@auth
def get_users():
    users = User.query.all()
    if not users:
        abort(404, "No users found.")
    return jsonify({"users": [x.serialized for x in users]}), 200


@api.route('/users/<int:id>', methods=['GET'])
@auth
def get_user(id):
    user = User.query.filter_by(id=id).all()
    if not user:
        abort(404, f'User {id} not found.')
    return jsonify({"users": [x.serialized for x in user]}), 200


@api.route('/users', methods=['POST'])
@auth
def create_user():
    data = request.json
    schema = user_schema.UserSchema()
    try:
        schema.load(data)
    except ValidationError:
        abort(400, "No data provided.")

    validations(data)

    user = User(name=data["name"], password=data["password"], admin=data["admin"])
    for group_id in data["group"]:
        group = Group.query.filter_by(id=group_id).first()
        if not group:
            abort(404, f"Group {group_id} not found.")
        user.group.append(group)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialized), 201


@api.route('/users/<int:id>', methods=['DELETE'])
@auth
def delete_user(id):
    user = User.query.get(id)
    if not user:
        abort(404, f"User {id} not found.")
    db.session.delete(user)
    db.session.commit()
    return jsonify({"status": True})


@api.route('/users/<int:id>', methods=['PUT'])
@auth
def update_user(id):
    data = request.json
    schema = user_schema.UserSchema()
    try:
        schema.load(data)
    except ValidationError:
        abort(400, "No data provided.")

    name = data.get("name")
    if not name:
        abort(400, "Required to enter valid name")
    password = data.get("password")
    admin = data.get("admin")

    user = User.query.get(id)

    if not user:
        abort(404, f"User {id} not found.")

    if name:
        user.name = name
    if password:
        user.password = password

    user.admin = admin

    group = data["group"]
    if group == [] or None:
        user.group.clear()
    else:
        for group_id in group:
            group = Group.query.filter_by(id=group_id).first()
            if not group:
                abort(404, f'Group {group_id} not found.')
            user.group.append(group)

    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialized)
