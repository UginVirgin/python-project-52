#!/usr/bin/env bash
set -o errexit

# Синхронизируем зависимости с помощью uv (Render сам предоставит uv)
uv sync --frozen

# Активируем виртуальное окружение, созданное uv
source .venv/bin/activate

# Собираем статические файлы
python manage.py collectstatic --no-input

# Применяем миграции базы данных
python manage.py migrate