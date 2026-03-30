#!/usr/bin/env bash
set -o errexit

# Устанавливаем uv (если его нет на сервере)
pip install uv

# Устанавливаем зависимости из pyproject.toml
uv pip install --system .

# Собираем статические файлы
python manage.py collectstatic --no-input

# Применяем миграции
python manage.py migrate