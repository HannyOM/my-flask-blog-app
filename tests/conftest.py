# This file contains setup functions called "Fixtures" that each test will use.
# Test files and Test functions begin with "test_".
# Each test will create a new temporary database file and populate some data that will be used in the tests.

import pytest
from bloggr import create_app 
from bloggr import db as _db            # Internal / Private database instance (for testing purposes only).
from bloggr import bcrypt as _bcrypt
from bloggr.models import User

# The app fixture will call the factory and pass "test_config" to configure the application and database for testing instead of using the local development configuration.
@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,            # Enables testing mode.
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"            # Uses an in-memory SQLite databse (fast, isolated and no clean up needed).
    })

    with app.app_context():         # Enters the Flask application context.
        _db.create_all()            # Creates all database tables.
        yield app           # Yields the app instance to tests (pauses here while tests run).
        _db.session.remove()            # Cleans up the database session.
        _db.drop_all()          # Drops all the database tables after tests are finished.

@pytest.fixture
def db(app):
    return _db

@pytest.fixture
def bcrypt():
    return _bcrypt

@pytest.fixture
def client(app):            # Creates a test client (simulates HTTP requests to the Flask app).
    return app.test_client()

@pytest.fixture
def create_user(db, bcrypt):
    username = "test_username"
    password = "test_password"
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(username=username, password=hashed_password) # type: ignore
    db.session.add(user)
    db.session.commit()
    return username, password, user

@pytest.fixture
def create_user2(db, bcrypt):
    username2 = "test_username2"
    password2 = "test_password2"
    hashed_password2 = bcrypt.generate_password_hash(password2).decode("utf-8")
    user2 = User(username=username2, password=hashed_password2) # type: ignore
    db.session.add(user2)
    db.session.commit()
    return username2, password2, user2

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username="test_username", password="test_password"):
        return self._client.post("/auth/login", data={"username" : username,
                                                      "password" : password})
    def logout(self):
        return self._client.get("/auth/logout")
    
@pytest.fixture
def auth(client):
    return AuthActions(client)