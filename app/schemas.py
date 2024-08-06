from marshmallow import ValidationError, Schema, fields, validate
from werkzeug.exceptions import BadRequest

class SignupSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=5))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))
    bio = fields.Str(required=False)


class SigninSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))
