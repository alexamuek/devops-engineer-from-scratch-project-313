import os
from pathlib import Path

from flask import (
    abort,
    jsonify,
    make_response,
    request,
    send_from_directory,
)

from app.repository import Links
from app.validator import parse_and_check_range, validate_body

repo = Links


def handlers(app):
    @app.get("/ping")
    def ping():
        return "pong", 200

    @app.get("/")
    def index():
        return send_from_directory(Path(app.root_path) / "public", "index.html")

    @app.get("/api/links")
    def links_index():
        start_end_string = request.args.get("range", default="[0,10]")
        (offset, limit) = parse_and_check_range(start_end_string)
        if offset is None:
            return {"detail": "Bad range"}, 400
        links = repo.get_links(offset, limit)
        total = repo.get_count()
        start = offset
        if limit == 0:
            end = offset
        else:
            end = min(offset + limit - 1, total - 1)
        response = make_response(jsonify(links))
        response.status_code = 200
        response.headers["Content-Range"] = f"links {start}-{end}/{total}"
        response.headers["Accept-Ranges"] = "bytes"
        return response

    @app.post("/api/links")
    def links_post():
        # извлекаем данные из формы
        link = request.get_json(silent=True)
        if not validate_body(link):
            return {"detail": {"message": "Invalid JSON body"}}, 422
        # сохраняем новую ссылку 
        short_url = f"{os.getenv("BASE_URL")}/r/{link["short_name"]}"
        result = repo.add_link(link["original_url"], 
            link["short_name"], short_url)
        if result:
            return result, 201
        else:
            return {"detail": {"message": "Short name already exists"}}, 422

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
        link = request.get_json(silent=True)
        if not validate_body(link):
            return {"detail": {"message": "Invalid JSON body"}}, 422
        # сохраняем новую ссылку 
        short_url = f"{os.getenv("BASE_URL")}/r/{link["short_name"]}"
        new_link = repo.update_link(id, link["original_url"], 
            link["short_name"], short_url)
        if new_link is None:
            abort(404)
        if new_link is False:
            return {"detail": {"message": "Short name already exists"}}, 422
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