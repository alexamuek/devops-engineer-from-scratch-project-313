-include .env
export

install:
	pip install uv
	uv sync --frozen
start:
	uv run gunicorn -w 4 -b 0.0.0.0:8080 --timeout 120 app.main:app
lint:
	uv run ruff check .
test:
	uv run pytest
build:
	docker build -t my-flask-app:latest .
run:
	docker run -d -p 8080:8080 --name my-flask-app --env-file .env my-flask-app:latest
run-local-postgress:
	docker run --name $(POSTGRES_CONTAINER_NAME) \
  		-e POSTGRES_USER=$(LOCAL_POSTGRES_USER) \
  		-e POSTGRES_PASSWORD=$(LOCAL_POSTGRES_PASSWORD) \
  		-e POSTGRES_DB=$(LOCAL_POSTGRES_DB) \
  		-p $(LOCAL_POSTGRES_PORT):5432 \
  		-d postgres