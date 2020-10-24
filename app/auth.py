from app import db, app, jsonify, request
from flask import Blueprint
from . import user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)


auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['POST'])
def login():
    if request.method=='POST':
        data = request.json
        userData = user.User.query.filter_by(email=data['email']).first()
        print(userData)
        if userData:
            if check_password_hash(userData.password, data['password']):
                db.session.add(userData)
                db.session.commit()
                userDetails = {}
                userDetails['name'] = userData.name
                userDetails['mobile'] = userData.mobile
                userDetails['email'] = userData.email
                access_token = create_access_token(identity = userData.email)
                refresh_token = create_refresh_token(identity = userData.email)
                return jsonify({'message' : 'User Loggedin Successfully', 'user': userDetails, 'access_token': access_token, 'refresh_token': refresh_token})
    return jsonify({'message' : 'Something went wrong'})

@auth_blueprint.route('/signup', methods=['POST'])
def signup():
    if request.method=='POST':
        data = request.get_json();
        hashed_password = generate_password_hash(data['password'], method='sha256')
        new_user = user.User(name=data['name'], mobile=data['mobile'], email=data['email'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'New User Created'})
    return jsonify({'message' : 'Something went wrong'}) 

@auth_blueprint.route('/token-refresh', methods=['POST'])
@jwt_refresh_token_required
def genrateNewAccessTokenFromRefreshToken():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity = current_user)
    return {'access_token': access_token}

