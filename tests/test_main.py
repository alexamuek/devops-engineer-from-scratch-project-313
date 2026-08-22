import os

import pytest
from dotenv import load_dotenv  # Импортируем dotenv

from app.main import Links, app

load_dotenv()  # Загрузка переменных окружения из файла .env

bad_answer_422 = {"detail": "Short name already exists"}
bad_answer_404 = {"detail": "Resource is not found"}
test_data = {
        "id": 1,
        "original_url": "https://example.com/long-url1",
        "short_name": "test",
        "short_url":  f"{os.getenv('BASE_URL')}test"
    }


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_root_404_answer(monkeypatch, client):
    response = client.get('/')
    assert response.status_code == 404
    assert response.json == bad_answer_404


def test_links_index(monkeypatch, client):
    test_data = [
        {"id": 1, 
        "original_url": "https://example.com/long-url1", 
        "short_name": "7777", 
        "short_url": f"{os.getenv('BASE_URL')}7777"
        },
        {"id": 2, 
        "original_url": "https://example.com/long-url2", 
        "short_name": "yout1", 
        "short_url": f"{os.getenv('BASE_URL')}yout1"
        }
    ]
    monkeypatch.setattr(Links, "get_links", lambda: test_data)
    
    response = client.get('/api/links')
    assert response.status_code == 200
    assert response.json == test_data


def test_links_show(monkeypatch, client):
    test_data = {
        "id": 1,
        "original_url": "https://example.com/long-url1",
        "short_name": "7777",
        "short_url": f"{os.getenv('BASE_URL')}7777"
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
        "short_url": f"{os.getenv('BASE_URL')}old_name"
    }
    monkeypatch.setattr(Links, "update_link", 
        lambda id, original_url, short_name, short_url: False)
    response = client.put('/api/links/10', 
        json={"original_url": test_data["original_url"], 
        "short_name": test_data["short_name"]})
    assert response.status_code == 422
    assert response.json == bad_answer_422


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