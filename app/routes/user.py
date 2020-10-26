from app import db, app, jsonify
from flask import Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required
from app.models.user import User

user_blueprint = Blueprint('user', __name__, url_prefix='/user')

@user_blueprint.route('/', methods=['GET'])
def get_all_users():
    users = User.query.all()
    Output = []
    for user in users:
        user_data = {}
        user_data['name'] = user.name
        user_data['mobile'] = user.mobile
        user_data['email'] = user.email
        Output.append(user_data)
    
    return jsonify({'users': Output})

@user_blueprint.route('/<id>', methods=['GET'])
@jwt_required
def get_user(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'message': 'No User Found'})

    user_data = {}
    user_data = {}
    user_data['name'] = user.name
    user_data['mobile'] = user.mobile
    user_data['email'] = user.email
    return jsonify(user_data)

@user_blueprint.route('/', methods=['POST'])
def create_user():
    data = request.get_json();
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(name=data['name'], mobile=data['mobile'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New User Created'})