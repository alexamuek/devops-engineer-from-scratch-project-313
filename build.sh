#!/usr/bin/env bash

set -a
source .env
set +a

# Ждём, пока БД запустится
sleep 3

# Выполняем init.sql с правильным пользователем
docker exec -i "$POSTGRES_CONTAINER_NAME" psql -d "$DATABASE_URL" < init.sql