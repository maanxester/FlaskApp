
from engine.app import app, db
from flask import jsonify, request, abort
from engine.app.models.users import User
from engine.app.models.groups import Group


@app.route('/users',  methods=['GET'])
def get_users():
    users = User.query.all()
    if not users:
        abort(404, "No users found.")
    return jsonify({"users": [x.serialized for x in users]}), 200


@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.filter_by(id=id).all()
    if not user:
        abort(404, f'User {id} not found.')
    return jsonify({"users": [x.serialized for x in user]}), 200


@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if not data:
        abort(400, "No data provided.")

    user = User(name=data["name"], password=data["password"], admin=data["admin"])
    for group_id in data["group"]:
        group = Group.query.filter_by(id=group_id).first()
        if not group:
            abort(404, f"Group {group_id} not found.")
        user.group.append(group)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialized), 201


@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        abort(404, f"User {id} not found.")
    db.session.delete(user)
    db.session.commit()
    return jsonify({"status": True})


@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    if not data:
        abort(400, 'No data provided.')

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





