### Hexlet tests and linter status:
[![Actions Status](https://github.com/UginVirgin/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/UginVirgin/python-project-52/actions)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=UginVirgin_python-project-52&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=UginVirgin_python-project-52)

# Task Manager (Менеджер задач)
Веб-приложение для управления задачами с аутентификацией, статусами, метками и CRUD-операциями. Проект выполнен в рамках учебного курса Hexlet.

## [Деплой проекта на Render.com](https://python-project-52-xcvi.onrender.com)

## Функциональность

- 🔐 **Аутентификация и авторизация** — регистрация, вход, выход, управление пользователями
- 📝 **Управление задачами** — создание, просмотр, редактирование, удаление задач
- 🏷️ **Статусы задач** — гибкая настройка статусов (например, "Новая", "В работе", "Завершена")
- 🏷️ **Метки (Labels)** — возможность добавлять метки к задачам для категоризации
- 👥 **Пользователи** — просмотр списка пользователей и профилей
- 🛡️ **Права доступа** — только автор или администратор может изменять/удалять задачу
- 🌐 **Интерфейс на русском языке** (с возможностью локализации)

## 🛠 Технологии

- Python 3.10+
- Django 6.0+
- SQLite (по умолчанию, легко меняется на PostgreSQL)
- Bootstrap 5 (через шаблоны)
- drf-yasg (документация API)
- python-dotenv (управление переменными окружения)

## 📦 Установка и запуск

### Клонировать репозиторий

```bash
git clone https://github.com/ваш-аккаунт/python-project-52.git
cd python-project-52
```

### 2. Создать виртуальное окружение

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# или
venv\Scripts\activate     # Windows
```


### 3. Установить зависимости

```bash
pip install -e .
# или
pip install -r requirements.txt  # если создадите файл
```

### 4. Настроить переменные окружения

```bash
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### 5. Применить миграции

```bash
make migrations
# или
python manage.py migrate
```

### 6. Запустить сервер

```bash
make run
# или
python manage.py runserver
```

### 7. Запуск тестов
```bash
python manage.py test
```

## 3. Использование

Регистрация — создайте нового пользователя
Создание статусов — перейдите в раздел "Статусы" → "Создать статус"
Создание меток — перейдите в раздел "Метки" → "Создать метку"
Создание задачи — заполните форму: название, описание, статус, исполнитель, метки
Управление задачами — доступны фильтры по статусу, исполнителю, меткам 

