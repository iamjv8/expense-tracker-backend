from app import db, app, jsonify, request
from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.models.group import Group, GroupMembers

group_blueprint = Blueprint('group', __name__)

@group_blueprint.route('/group',methods=['POST'])
@jwt_required
def create_group():
    data = request.get_json();
    new_group = Group(group_name=data['group_name'], group_type=data['group_type'], icon=data['icon'])
    db.session.add(new_group)
    db.session.commit()
    return jsonify({'message': 'New Group Created'})

@group_blueprint.route('/group/<id>',methods=['GET'])
@jwt_required
def get_group(id):
    result = db.session.query(Group, GroupMembers).join(Group).filter(GroupMembers.group_id == id).all()
    group_data = {}
    group_data['members'] = list()
    for group, members in result:
        group_data['id'] = group.id
        group_data['group_name'] = group.group_name
        group_data['icon'] = group.icon
        group_data['members'].append({'name': members.user_name, 'mobile': members.user_mobile})

    if not group_data:
        return jsonify({'message': 'No Group Found'})
    return (jsonify(group_data))

@group_blueprint.route('/group/members', methods=['POST'])
@jwt_required
def add_members_in_group():
    data = request.get_json()
    print(data['members'])
    members = []
    for member in data['members']:
        members.append(GroupMembers(user_mobile=member['mobile'], user_name=member['name'], group_id=data['group_id']))
    db.session.bulk_save_objects(members);
    db.session.commit()
    return jsonify({'message': 'Members added successfully'});

    