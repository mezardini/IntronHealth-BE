from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import db


# This is the user model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    bio = db.Column(db.String(200),  nullable=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


# This is the model to store blacklisted tokens
class TokenBlacklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    token_type = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    revoked = db.Column(db.Boolean, nullable=False, default=True)
    expires = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"TokenBlacklist('{self.jti}', '{self.token_type}', '{self.user_id}', '{self.revoked}', '{self.expires}')"

