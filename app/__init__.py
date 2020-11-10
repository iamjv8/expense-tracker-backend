from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import uuid
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/expense_tracker'

# initialize sql-alchemy
db = SQLAlchemy(app)

jwt = JWTManager(app)

#register Blueprints
from .routes import user
app.register_blueprint(user.user_blueprint)

from .routes import auth
app.register_blueprint(auth.auth_blueprint)

from .routes import group
app.register_blueprint(group.group_blueprint)
