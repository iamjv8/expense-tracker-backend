from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import uuid
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/expense_tracker'


# initialize sql-alchemy
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    mobile = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)

@app.route('/user', methods=['GET'])
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

@app.route('/user/<id>', methods=['GET'])
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

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json();
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(name=data['name'], mobile=data['mobile'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New User Created'})