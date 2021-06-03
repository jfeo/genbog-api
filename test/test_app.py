import json

import pytest

from genbog.app import create_app


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client


def test_delete_idempotent(client):
    # post a few books to get some data
    client.post("/books/1234567890123")
    client.post("/books/1234567890123")
    client.post("/books/1234567890123")

    r = client.delete("/books/1234567890123")
    assert r.status_code == 200
    data = json.loads(r.data)
    assert len(data.keys()) == 2
    assert "isbn" in data
    assert "count" in data
    assert data["isbn"] == "1234567890123"
    assert data["count"] == 2

    r = client.delete("/books/1234567890123")
    assert r.status_code == 200
    data = json.loads(r.data)
    assert len(data.keys()) == 2
    assert "isbn" in data
    assert "count" in data
    assert data["isbn"] == "1234567890123"
    assert data["count"] == 1

    # no matter how many times we delete, count is 0
    for _ in range(100):
        r = client.delete("/books/1234567890123")
        assert r.status_code == 200
        data = json.loads(r.data)
        assert len(data.keys()) == 2
        assert "isbn" in data
        assert "count" in data
        assert data["isbn"] == "1234567890123"
        assert data["count"] == 0


def test_delete_invalid_isbn(client):
    r = client.delete("/books/123")
    assert r.status_code == 400

    r = client.delete("/books/abcdefghijkln")
    assert r.status_code == 400

    r = client.delete("/books/12345678901234")
    assert r.status_code == 400


def test_get_valid_non_existing_isbn_is_zero(client):
    r = client.get("/books/3210987654321")
    assert r.status_code == 200

    data = json.loads(r.data)
    assert len(data.keys()) == 2
    assert "isbn" in data
    assert "count" in data
    assert data["isbn"] == "3210987654321"
    assert data["count"] == 0


def test_get_data_equal_to_post_data(client):
    for i in range(1, 100):
        post_r = client.post("/books/1234567890123")
        assert post_r.status_code == 200
        post_data = json.loads(post_r.data)
        assert "isbn" in post_data
        assert "count" in post_data
        assert post_data["isbn"] == "1234567890123"
        assert post_data["count"] == i

        get_r = client.get("/books/1234567890123")
        assert get_r.status_code == 200
        get_data = json.loads(get_r.data)
        assert "isbn" in get_data
        assert "count" in get_data
        assert get_data["isbn"] == "1234567890123"
        assert get_data["count"] == i


def test_get_list_returns_all_posted(client):
    client.post("/books/1112223334444")
    client.post("/books/1112223334444")
    client.post("/books/1112223334444")
    client.post("/books/1112223334444")
    client.post("/books/2223334444111")
    client.post("/books/1231231231234")
    client.post("/books/1231231231234")
    r = client.get("/books")
    assert r.status_code == 200
    data = json.loads(r.data)
    assert len(data) == 3
    assert any(r["isbn"] == "1112223334444" and r["count"] == 4 for r in data)
    assert any(r["isbn"] == "2223334444111" and r["count"] == 1 for r in data)
    assert any(r["isbn"] == "1231231231234" and r["count"] == 2 for r in data)


def test_get_list_not_returns_deleted(client):
    client.post("/books/1112223334444")
    client.post("/books/1112223334444")
    client.post("/books/1112223334444")
    client.delete("/books/1112223334444")
    client.delete("/books/1112223334444")
    client.delete("/books/1112223334444")
    r = client.get("/books")
    assert r.status_code == 200
    data = json.loads(r.data)
    assert len(data) == 0


def test_get_invalid_isbn(client):
    r = client.get("/books/123")
    assert r.status_code == 400

    r = client.get("/books/abcdefghijkln")
    assert r.status_code == 400

    r = client.get("/books/12345678901234")
    assert r.status_code == 400


def test_post_list_invalid_isbn_error(client):
    r = client.post("/books", json=["123"])
    assert r.status_code == 400

    r = client.post("/books", json=["1231231231234", "123"])
    assert r.status_code == 400

    r = client.post("/books", json=["123", "1231231231234"])
    assert r.status_code == 400


def test_post_list_invalid_isbn_atomic(client):
    r = client.get("/books")
    data = json.loads(r.data)
    assert len(data) == 0

    r = client.post("/books", json=["1231231231234", "123", "1112223334444"])
    assert r.status_code == 400

    r = client.get("/books")
    data = json.loads(r.data)
    assert len(data) == 0


def test_post_list_return_current_counts(client):
    client.post("/books/1231231231234")
    client.post("/books/1231231231234")

    r = client.post("/books", json=["1231231231234", "1112223334444"])
    assert r.status_code == 200
    data = json.loads(r.data)
    assert len(data) == 2
    assert any(r["isbn"] == "1112223334444" and r["count"] == 1 for r in data)
    assert any(r["isbn"] == "1231231231234" and r["count"] == 3 for r in data)


def test_post_list_add_all_same(client):
    r = client.get("/books")
    data = json.loads(r.data)
    assert len(data) == 0

    r = client.post("/books", json=["1231231231234", "1231231231234"])
    assert r.status_code == 200

    r = client.get("/books")
    data = json.loads(r.data)
    assert len(data) == 1
    assert len(data[0].keys()) == 2
    assert data[0]["isbn"] == "1231231231234"
    assert data[0]["count"] == 2


def test_post_invalid_isbn(client):
    r = client.post("/books/123")
    assert r.status_code == 400

    r = client.post("/books/abcdefghijkln")
    assert r.status_code == 400

    r = client.post("/books/12345678901234")
    assert r.status_code == 400
