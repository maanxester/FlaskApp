
from engine.app import app, db
from engine.app.resources.api import api
from flask import request, abort, jsonify
from engine.app.models.users import User
from engine.app.models.groups import Group
from engine.app.schemas.group_schema import GroupSchema, ValidationError


def validations(data):
    name = data.get("name")
    if not name:
        abort(400, "Name is required.")


@api.route('/groups', methods=['GET'])
def get_groups():
    groups = Group.query.all()
    if not groups:
        abort(404, "Groups not found.")
    return jsonify({"groups": [x.serialized for x in groups]})


@api.route('/groups/<int:id>', methods=['GET'])
def get_group(id):
    group = Group.query.filter_by(id=id).all()
    if not group:
        abort(404, f'Group {id} not found.')
    return jsonify({"group": [x.serialized for x in group]})


@api.route('/groups', methods=['POST'])
def create_group():
    data = request.json
    schema = GroupSchema()
    try:
        schema.load(data)
    except ValidationError:
        abort(400, "No data provided.")

    validations(data)

    group = Group(name=data["name"])
    for user_id in data["user"]:
        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(404, f'User {user_id} not found.')
        group.user.append(user)
    db.session.add(group)
    db.session.commit()
    return jsonify(group.serialized), 201


@api.route('/groups/<int:id>', methods=['DELETE'])
def delete_group(id):
    group = Group.query.get(id)
    if not group:
        abort(404, f'Group not found.')
    db.session.delete(group)
    db.session.commit()
    return jsonify({"status": True})


@api.route('/groups/<int:id>', methods=['PUT'])
def update_group(id):

    data = request.json
    schema = GroupSchema()
    try:
        schema.load(data)
    except ValidationError:
        abort(400, "No data provided.")

    name = data.get("name")
    if not name:
        abort(400, "Name is required")

    group = Group.query.get(id)
    if not group:
        abort(404, f"Group {id} not found.")

    if name:
        group.name = name

    user = data["user"]
    if user == [] or None:
        group.user.clear()
    else:
        for user_id in user:
            user = User.query.filter_by(id=user_id).first()
            if not user:
                abort(404, f'User {user} not found.')
            group.user.append(user)

    db.session.add(group)
    db.session.commit()
    return jsonify(group.serialized), 200




