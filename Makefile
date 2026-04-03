setup:
	pip install -r requirements.txt
	python manage.py migrate
	npx playwright install chromium --with-deps

test:
	npx playwright install chromium --with-deps
	python manage.py test
	npx playwright test

run:
	python manage.py runserver 0.0.0.0:8000

lint:
	ruff check .

lint-fix:
	ruff check --fix .