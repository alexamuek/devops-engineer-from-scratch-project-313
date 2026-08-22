import os

from dotenv import load_dotenv  # Импортируем dotenv
from flask import Flask, abort, jsonify, make_response, request

from app.instruments import sentry_init
from app.repository import Links

sentry_init()

load_dotenv()  # Загрузка переменных окружения из файла .env

# Это callable WSGI-приложение
app = Flask(__name__)
app.secret_key = os.getenv("SECRET")
app.logger.setLevel("INFO")

repo = Links

bad_answer = {"error": "Short name already exists"}


@app.get("/api/links")
def links_index():
    links = repo.get_links()
    return jsonify(links), 200


@app.post("/api/links")
def links_post():
    # извлекаем данные из формы
    link = request.json
    # сохраняем новую ссылку 
    short_url = f"{os.getenv("BASE_URL")}{link["short_name"]}"
    result = repo.add_link(link["original_url"], 
        link["short_name"], short_url)
    if result:
        return result, 201
    else:
        return bad_answer, 422


@app.get("/api/links/<int:id>")
def links_show(id):
    link = repo.find_link_by_id(id)
    if link:
        return jsonify(link), 200
    else:
        abort(404)


@app.delete("/api/links/<int:id>")
def links_delete(id):
    link = repo.delete_link(id)
    if link:
        return "", 204
    else:
        abort(404)


@app.put("/api/links/<int:id>")
def links_patch(id):
    link = request.json
    # сохраняем новую ссылку 
    short_url = f"{os.getenv("BASE_URL")}{link["short_name"]}"
    new_link = repo.update_link(id, link["original_url"], 
        link["short_name"], short_url)
    if new_link is None:
        abort(404)
    if new_link is False:
        return bad_answer, 422
    return jsonify(new_link), 200
        

@app.get("/r/<short_name>")
def links_redirect(short_name):
    link = repo.find_link_by_short_name(short_name)
    if link is None:
        abort(404)
    response = make_response()
    response.status_code = 302
    response.headers["Location"] = link["original_url"]
    return response


@app.errorhandler(404)
def not_found(error):
    return "Not Found", 404

# uv run flask --app app.main run --port 8080  - запуск development сервера