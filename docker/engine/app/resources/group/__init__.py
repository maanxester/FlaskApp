
from engine.app import app, db
from flask import request, abort, jsonify
from engine.app.models.users import User
from engine.app.models.groups import Group


@app.route('/groups', methods=['GET'])
def get_groups():
    groups = Group.query.all()
    if not groups:
        abort(404, "Groups not found.")
    return jsonify({"groups": [x.serialized for x in groups]})


@app.route('/group/<int:id>', methods=['GET'])
def get_group(id):
    group = Group.query.get(id)
    if not group:
        abort(404, f'Group {id} not found.')
    return jsonify({"group": [x.serialized for x in group]})


@app.route('/groups', methods=['POST'])
def create_group():
    data = request.json
    if not data:
        abort(400, 'No data provided.')

    group = Group(name=data["name"])
    for user_id in data["user"]:
        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(404, f'User {user_id} not found.')
        group.user.append(user)
    db.session.add(group)
    db.session.commit()
    return jsonify(group.serialized), 201


@app.route('/groups/<int:id>', methods=['DELETE'])
def delete_group(id):
    group = Group.query.get(id)
    if not group:
        abort(404, f'Group {group} not found.')
    db.session.delete(group)
    db.session.commit()
    return jsonify({"status": True})


@app.route('/groups/<int:id>', methods=['PUT'])
def update_group(id):

    data = request.json
    if not data:
        abort(400, 'No data provived.')

    name = data.get("name")
    if name == '':
        abort(400, "Required to enter valid name")

    group = Group.query.get(id)
    if not group:
        abort(404, f"Group {id} not found.")

    if name:
        group.name = name

    user_id = data.get("user")
    if user_id == [] or None:
        group.user.clear()
    else:
        x = User.query.filter_by(id=user_id).all()
        if not x:
            abort(404, f'User {x} not found.')
        group.user.append(x)

    db.session.add(group)
    db.session.commit()
    return jsonify(group.serialized), 200




