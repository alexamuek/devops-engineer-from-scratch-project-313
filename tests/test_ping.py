import requests


def test_ping():
	response = requests.get("http://0.0.0.0:8080/ping")
	assert response.text == "pong"
	assert response.status_code == 200


def test_other():
	response = requests.get("http://0.0.0.0:8080/1")
	assert response.text == "Page not found"
	assert response.status_code == 404
