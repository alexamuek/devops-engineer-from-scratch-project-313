import os

import pytest
from dotenv import load_dotenv  # Импортируем dotenv

from app.main import Links, app

load_dotenv()  # Загрузка переменных окружения из файла .env

bad_answer_422 = {"detail": {"message": "Short name already exists"}}
bad_answer_404 = {"detail": "Resource is not found"}
bad_answer_for_validation = {"detail": {"message":"Invalid JSON body"}}

test_data = {
        "id": 1,
        "original_url": "https://example.com/long-url1",
        "short_name": "test",
        "short_url":  f"{os.getenv('BASE_URL')}/r/test"
    }


@pytest.fixture
def make_test_data():
    def factory(records):
        result = [{
            "id": i,
            "original_url": f"https://example.com/long-url{i}",
            "short_name": f"test{i}",
            "short_url":  f"{os.getenv('BASE_URL')}/r/test{i}"
        } for i in range(records)]
        return result
    return factory


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_root_200_answer(monkeypatch, client):
    response = client.get('/')
    assert response.status_code == 200


def test_links_index(monkeypatch, client, make_test_data):
    records = 2
    test_data = make_test_data(records)
    monkeypatch.setattr(Links, "get_links", lambda offset_, limit_: test_data)
    total = 10
    monkeypatch.setattr(Links, "get_count", lambda: total)
    range_param = "range=[0,2]"
    response = client.get(f"/api/links?{range_param}")
    assert response.status_code == 200
    assert response.headers["Content-Range"] == "links 0-1/10"
    assert response.headers["Accept-Ranges"] == "bytes"
    assert response.json == test_data


def test_links_index_bad_range(monkeypatch, client):
    test_data = []
    cases = ["range=[2,1]", "range=[-1,1]", "range=[b,1]", "range=[0,1"]
    monkeypatch.setattr(Links, "get_links", lambda offset_, limit_: test_data)
    monkeypatch.setattr(Links, "get_count", lambda: 2)
    for r in cases:
        response = client.get(f"/api/links?{r}")
        assert response.status_code == 400
        assert response.json == {"detail": "Bad range"}


def test_links_index_empty_range(monkeypatch, client):
    test_data = []
    monkeypatch.setattr(Links, "get_links", lambda offset_, limit_: test_data)
    monkeypatch.setattr(Links, "get_count", lambda: 2)
    range_param = "range=[0,0]"
    response = client.get(f"/api/links?{range_param}")
    assert response.status_code == 200
    assert response.json == test_data
    assert response.headers["Content-Range"] == "links 0-0/2"


def test_links_index_default_range(monkeypatch, client, make_test_data):
    records = 10
    test_data = make_test_data(records)
    monkeypatch.setattr(Links, "get_links", lambda offset_, limit_: test_data)
    monkeypatch.setattr(Links, "get_count", lambda: 2)
    response = client.get("/api/links")
    assert response.status_code == 200
    assert response.headers["Content-Range"] == "links 0-1/2"
    assert response.json == test_data


def test_links_show(monkeypatch, client):
    test_data = {
        "id": 1,
        "original_url": "https://example.com/long-url1",
        "short_name": "7777",
        "short_url": f"{os.getenv('BASE_URL')}/r/7777"
    }
    monkeypatch.setattr(Links, "find_link_by_id", lambda id: test_data)
    response = client.get('/api/links/1')
    assert response.status_code == 200
    assert response.json == test_data


def test_links_show_404_answer(monkeypatch, client):
    monkeypatch.setattr(Links, "find_link_by_id", lambda id: None)
    response = client.get('/api/links/10')
    assert response.status_code == 404
    assert response.json == bad_answer_404


def test_links_delete(monkeypatch, client):
    monkeypatch.setattr(Links, "delete_link", lambda id: True)
    response = client.delete('/api/links/1')
    assert response.status_code == 204
    assert response.text == ""


def test_links_delete_404_answer(monkeypatch, client):
    monkeypatch.setattr(Links, "delete_link", lambda id: None)
    response = client.delete('/api/links/10')
    assert response.status_code == 404
    assert response.json == bad_answer_404


def test_links_patch(monkeypatch, client):
    monkeypatch.setattr(Links, "update_link", 
        lambda id, original_url, short_name, short_url: test_data)
    response = client.put('/api/links/1', 
        json={"original_url": test_data["original_url"], 
            "short_name": test_data["short_name"]})
    assert response.status_code == 200
    assert response.json == test_data


def test_links_patch_404_answer(monkeypatch, client):
    monkeypatch.setattr(Links, "update_link", 
        lambda id, original_url, short_name, short_url: None)
    response = client.put('/api/links/10', 
        json={"original_url": test_data["original_url"], 
            "short_name": test_data["short_name"]})
    assert response.status_code == 404
    assert response.json == bad_answer_404


def test_links_patch_422_answer(monkeypatch, client):
    test_data = {
        "id": 1,
        "original_url": "https://example.com/long-url1",
        "short_name": "exicted_name",
        "short_url": f"{os.getenv('BASE_URL')}/r/old_name"
    }
    monkeypatch.setattr(Links, "update_link", 
        lambda id, original_url, short_name, short_url: False)
    response = client.put('/api/links/1', 
        json={"original_url": test_data["original_url"], 
        "short_name": test_data["short_name"]})
    assert response.status_code == 422
    assert response.json == bad_answer_422


def test_links_patch_422_validation_empty(monkeypatch, client):
    response = client.put('/api/links/1', 
        json={})
    assert response.status_code == 422
    assert response.json == bad_answer_for_validation


def test_links_patch_422_validation(monkeypatch, client):
    response = client.put('/api/links/1', 
        json={"url": "test_url", 
        "name": "test_name"})
    assert response.status_code == 422
    assert response.json == bad_answer_for_validation


def test_links_post(monkeypatch, client):
    monkeypatch.setattr(Links, "add_link", 
        lambda original_url, short_name, short_url: test_data)
    response = client.post('/api/links', 
        json={"original_url": test_data["original_url"], 
            "short_name": test_data["short_name"]})
    assert response.status_code == 201
    assert response.json == test_data


def test_links_post_422_answer(monkeypatch, client):
    monkeypatch.setattr(Links, "add_link", 
        lambda original_url, short_name, short_url: None)
    response = client.post('/api/links', 
        json={"original_url": test_data["original_url"], 
            "short_name": test_data["short_name"]})
    assert response.status_code == 422
    assert response.json == bad_answer_422


def test_links_post_422_validation_empty(monkeypatch, client):
    response = client.post('/api/links', 
        json={})
    assert response.status_code == 422
    assert response.json == bad_answer_for_validation


def test_links_post_422_validation(monkeypatch, client):
    response = client.post('/api/links', 
        json={"url": "test_url", 
            "name": "test_name"})
    assert response.status_code == 422
    assert response.json == bad_answer_for_validation


def test_links_redirect_by_short_name_404_answer(monkeypatch, client):
    monkeypatch.setattr(Links, "find_link_by_short_name", 
        lambda short_name: None)
    response = client.get('/r/test')
    assert response.status_code == 404
    assert response.json == bad_answer_404


def test_links_redirect_by_short_name(monkeypatch, client):
    monkeypatch.setattr(Links, "find_link_by_short_name", 
        lambda short_name: test_data)
    response = client.get('/r/test')
    assert response.status_code == 302
    assert response.headers["Location"] == test_data["original_url"]