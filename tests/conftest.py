import pytest
from app import create_app, db


@pytest.fixture(scope='module')
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture(scope='module')
def client(app):
    return app.test_client()
