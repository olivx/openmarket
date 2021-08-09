SHELL := /bin/sh
TAG := git rev-parse --short HEAD
IMAGE_NAME := openmarket

help:
	@echo 'Usage:'
	@echo 'make docker-start:		Run docker compose used command docker-compose up --build'
	@echo 'make docker-stop:		Run stop docker compose used command docker-compose down'
	@echo 'make build:			Run docker build image'
	@echo 'make dump_data:			Run load data to data base'
	@echo 'make format:			Run black format flak8 and isort'
	@echo 'make run:			Run run open market application dev server'
	@echo 'make clean:			Clean directory deleting file such as .pyc .swp and __pycache__'
	@echo 'make test:			Run test with pytest coverage'
	@echo 'make lint:			Check lint flak8'
	@echo 'make makemigrations:		Run python manage.py makemigrations'
	@echo 'make migrate:			Run python manage.py migrate'
	@echo 'make runserver:			Run python manage.py runserver'
	@echo ''

clean:
	@rm -f .coverage 2> /dev/null
	@rm -rf .cache 2> /dev/null
	@find . -name "*.pyc" -delete
	@find . -name "*.swp" -delete
	@find . -name "__pycache__" -delete

sort:
	@isort .

format:
	make sort
	@black api

lint:
	@flake8 api

test: clean lint
	export DATABASE_URL="postgis://postgres:secret@localhost:5432/test"
	docker run --name=postgis_tests -d -e POSTGRES_USER=postgres -e POSTGRES_PASS=postgres -e POSTGRES_DBNAME=open-market_tests -p 5432:5432 kartoza/postgis:13.0
	sleep 5
	python -m pytest --cov=api --cov=openmarket
	docker container rm -f postgis_tests
	unset DATABASE_URL

dump_data:
	python manage.py load_data -f contrib/open-markets-data.csv

run:
	python manage.py runserver

docker-start:
	docker-compose up --build

docker-stop:
	docker-compose down

build:
	poetry export --without-hashes --no-interaction --no-ansi -f requirements.txt -o requirements.txt
	docker build -t $(IMAGE_NAME):$(TAG) .

build-dev:
	poetry export --without-hashes --no-interaction --no-ansi -f requirements.txt -o requirements.txt
	docker build -t $(IMAGE_NAME):lastest -f Dockerfile.dev .

run-postgres:
	 docker run --name=postgis -d -e POSTGRES_USER=postgres -e POSTGRES_PASS=postgres -e POSTGRES_DBNAME=open-market -p 5432:5432 kartoza/postgis:13.0

runserver:
	python manage.py runserver

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations