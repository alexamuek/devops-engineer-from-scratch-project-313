FROM python:3.14-slim

# Обновляем список пакетов и устанавливаем make
RUN apt-get update && apt-get install -y --no-install-recommends nginx \
    make \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями отдельно для лучшего кэширования
COPY pyproject.toml uv.lock Makefile ./
COPY services/nginx/nginx.conf /etc/nginx/conf.d/default.conf
RUN rm -f /etc/nginx/sites-enabled/default

RUN make install

# Копируем весь код приложения
COPY . .

# Запускаем сервер при старте контейнера
CMD ["make", "start-with-nginx"]