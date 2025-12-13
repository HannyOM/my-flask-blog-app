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