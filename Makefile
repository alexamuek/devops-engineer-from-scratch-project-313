install:
	pip install uv
	uv sync --frozen
start:
	uv run gunicorn -w 4 -b 0.0.0.0:8080 --timeout 120 main:app
lint:
	uv run ruff check .
test:
	uv run pytest
build:
	docker build -t my-flask-app:latest .
run:
	docker run -p 8080:8080 --name my-flask-app --env-file .env my-flask-app:latest