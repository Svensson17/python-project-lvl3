lint:
	poetry run flake8 page_loader

build:
	poetry build

package-install:
	poetry install

test-coverage:
	poetry runn pytest --cov=page_loader --cov-report xml