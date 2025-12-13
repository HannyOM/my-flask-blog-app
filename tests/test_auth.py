import pytest
from bloggr.models import User

def test_register(client, app):
    test_register_page_status = client.get("/auth/register").status_code            # Simulates a GET request to get the "Register" page.  
    assert test_register_page_status == 200         # Asserts that the request was successful.
    
    response = client.post("/auth/register", data={"username" : "test_username",            # Simulates a POST request to the "Register" page, converting the "data" dictionary into form data. 
                                                   "password" : "test_password"})
    assert response.headers["Location"] == "/auth/login"            # Asserts that the client will be redirected to "/auth/login" if successful. 
    
    with app.app_context():
        existing_user = User.query.filter_by(username="test_username").first()
    assert existing_user is not None


@pytest.mark.parametrize(("username", "password", "message"),(("", "", b"Username is required."),           # Tells Pytest to run the same test function with different arguments.
                                                              ("test_username", "", b"Password is required."),
                                                              ("existing_test_username", "existing_test_password", b"User already exists.")))
def test_register_validate_input(client, app, db, username, password, message):
    with app.app_context():
        user = User(username="existing_test_username", password="existing_test_password")           # type: ignore
        db.session.add(user)
        db.session.commit()
    response = client.post("/auth/register", data={"username" : username,
                                                   "password" : password})
    assert message in response.data


def test_login(client, create_user):
    test_login_page_status = client.get("/auth/login").status_code            
    assert test_login_page_status == 200

    username, password, user = create_user
    response = client.post("/auth/login", 
                           data={"username" : username, 
                                 "password" : password})
    assert response.headers["Location"] == "/" 
    
    with client.session_transaction() as sesh:          # Creates a context manager to access the Flask.
        user_id = sesh.get("_user_id")          # Gets the "_user_id" which is the default key Flask_Login uses to store the logged-in user's ID in the session.
        assert user_id == "1"           # Asserts user_id is "1" since that is the first user in the test database.


@pytest.mark.parametrize(("username", "password", "message"), (("", "", b"Username is required."), 
                                                               ("test_username", "", b"Password is required."), 
                                                               ("test_username", "wrong_test_password", b"Password is incorrect."),
                                                               ("wrong_test_username", "test_password", b"Username does not exist.")))
def test_login_validate_input(client, create_user, username, password, message):
    _username, _password, _user = create_user         
    response = client.post("/auth/login", data={"username" : username, 
                                                "password" : password})
    assert message in response.data


def test_logout(client, create_user):
    username, password, user = create_user
    client.post("/auth/login", data={"username" : username, 
                                     "password" : password})
    client.get("/auth/logout")
    with client.session_transaction() as sesh:
        user_id = sesh.get("_user_id")
        assert user_id is None