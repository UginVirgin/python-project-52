run:
	python manage.py runserver

migrations:
	python manage.py migrate

make lint:
	ruff check .

make lint-fix:
	ruff check --fix .

test:
	python manage.py test -v 2