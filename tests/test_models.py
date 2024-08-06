import pytest
from app.models import User 
from flask_sqlalchemy import SQLAlchemy

from app import create_app, db


def test_user_model(client):
    
    user = User(username='testuser', email='test@example.com', password='password', bio='Test bio')
    
    # Add the user to the test.db database
    db.session.add(user)
    db.session.commit()

    # Query the user from the test.db database
    queried_user = User.query.filter_by(email='test@example.com').first()


    assert queried_user is not None
    assert queried_user.username == 'testuser'
    assert queried_user.email == 'test@example.com'
    assert queried_user.bio == 'Test bio'
