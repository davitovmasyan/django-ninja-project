# Check if docker-compose or docker compose is available
DCOMPOSE = $(shell command -v docker-compose 2> /dev/null || echo docker compose)

RUN=${DCOMPOSE} run --rm project
COMMIT=$(shell git rev-parse --short HEAD)
DOCKER_REPO?=ghcr.io/davitovmasyan

all:
	${DCOMPOSE} build

run:
	${DCOMPOSE} run --service-ports --rm project

shell:
	${DCOMPOSE} run --rm project /bin/bash

stop:
	${DCOMPOSE} down

migrate:
	$(RUN) ./manage.py migrate

check:
	$(RUN) ./manage.py check

lint:
	$(RUN) ruff check .

test:
	$(RUN) pytest -x -vvv --create-db --cov=apps/ --ds=project.settings.test apps/

extract:
	${DCOMPOSE} run --rm packages cp -r  /usr/local/lib/python3.12/site-packages /host

mode:
	find . -type f -path './apps/*migrations*/*' -name '*.py' -exec chmod 0777 {} \;

start-mail:
	${DCOMPOSE} up mailhog

push:
	docker tag django-ninja-project-backend:latest ${DOCKER_REPO}/django-ninja-project-backend:${COMMIT}
	docker push ${DOCKER_REPO}/django-ninja-project-backend:${COMMIT}
	echo "Image pushed to ${DOCKER_REPO}/django-ninja-project-backend:${COMMIT}"
