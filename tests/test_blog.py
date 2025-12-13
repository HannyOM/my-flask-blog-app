import pytest
from bloggr.models import Post


def test_index(client, create_user, auth):
    response = client.get("/")
    assert b"New Post" in response.data

    # create_user # type: ignore
    auth.login()
    response = client.get("/")
    print(response.data)
    assert response.status_code == 200
    assert b"Welcome" in response.data


@pytest.mark.parametrize(("path", "method"), (("/new", "GET"), 
                                              ("/add", "POST"), 
                                              ("/edit/1", "GET"), 
                                              ("/save/1", "POST"), 
                                              ("/delete/1", "GET")))

def test_login_required(client, path, method):
    if method == "GET":
        response = client.get(path)
    else:
        response = client.post(path)
    assert response.headers["Location"].startswith("/auth/login")


