from marshmallow import ValidationError, Schema, fields, validate
from werkzeug.exceptions import BadRequest
from flask import jsonify, abort, request, Blueprint
from marshmallow import ValidationError
from .models import User, TokenBlacklist
from app import db, bcrypt
from flask_login import login_user, logout_user, login_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
from datetime import datetime, timezone, timedelta
from .schemas import SignupSchema, SigninSchema

bp = Blueprint('user', __name__)
jwt = JWTManager()


# This route is to get all users
@bp.route('/users/')
def get_users():
    users = User.query.all()
    users_list = [{'username': user.username, 'email': user.email, 'bio':user.bio}
                  for user in users]
    return jsonify(users_list), 200


# This route is to get a user by their username
@bp.route('/user/<string:username>/')
def get_user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    user_data = {
        'username': user.username,
        'email': user.email,
        'bio': user.bio
    }
    return jsonify(user_data), 200


# This route is to sign up a user
@bp.route('/signup/', methods=['POST'])
def signup():
    schema = SignupSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Check if the email already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already registered'}), 400

    # This is to hash the password
    hashed_password = bcrypt.generate_password_hash(
        data['password']).decode('utf-8')

    user = User(username=data['username'],
                email=data['email'], password=hashed_password, bio=data['bio'])

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201


# This route is to sign in a user
@bp.route('/signin/', methods=['POST'])
def signin():
    schema = SigninSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    email = data['email']
    password = data['password']

    # Check if the email exists
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)

        #This is to generate access and refresh tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401


# This route is to sign out a user
@bp.route('/signout/')
def signout():
    jti = get_jwt()['jti']
    expires = get_jwt()['exp']
    token = TokenBlacklist(jti=jti, token_type='access', user_id=get_jwt_identity(
    ), expires=datetime.fromtimestamp(expires, timezone.utc))
    db.session.add(token)
    db.session.commit()
    return jsonify({'message': 'Successfully logged out'}), 200
