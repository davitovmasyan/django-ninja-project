# django-ninja-project-backend
Backend application for django ninja project

### Development setup

Project requires to have `docker` and `docker-compose` cli tools available on machine.

Copy `.env_template` to `.env` file.

Modify `.env` file contents based on your needs.

Build docker image

    make

Run project in docker container(s)

    make run

### Development tooling setup

Extract `site-packages` from docker container using

    make extract

command.

In your IDE mark `apps` and `site-packages` folders as source folders.

### Other handy commands

Run tests

    make test

Run migrations

    make migrate

Run linter

    make lint

Jump into container

    make shell
