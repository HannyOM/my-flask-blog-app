# This file contains setup functions called "Fixtures" that each test will use.
# Test files and Test functions begin with "test_".
# Each test will create a new temporary database file and populate some data that will be used in the tests.

import pytest
from bloggr import create_app 
from bloggr import db as _db            # Internal / Private database instance (for testing purposes only).
from bloggr import bcrypt as _bcrypt

# The app fixture will call the factory and pass "test_config" to configure the application and database for testing instead of using the local development configuration.
@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,            # Enables testing mode.
        "SQL_DATABASE_URI": "sqlite:///:memory:"            # Uses an in-memory SQLite databse (fast, isolated and no clean up needed).
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

