install:
	pip install uv
	uv sync --frozen
run:
	uv run gunicorn -w 4 -b 0.0.0.0:8080 --timeout 120 main:app
lint:
	uv run ruff check .
test:
	uv run pytest