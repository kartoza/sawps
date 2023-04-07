export COMPOSE_FILE=deployment/docker-compose.yml:deployment/docker-compose.override.yml
SHELL := /bin/bash

build:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Building in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose build

build-dev:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Building in dev mode"
	@echo "------------------------------------------------------------------"
	@docker-compose build dev

wait-db:
	@docker-compose ${ARGS} exec -T db su - postgres -c "until pg_isready; do sleep 5; done"

create-test-db:
	@docker-compose ${ARGS} exec -T db su - postgres -c "psql -c 'create database test_db;'"

sleep:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Sleep for 10 seconds"
	@echo "------------------------------------------------------------------"
	@sleep 10
	@echo "Done"

up:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose ${ARGS} up -d nginx django

dev:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running in dev mode"
	@echo "------------------------------------------------------------------"
	@docker-compose ${ARGS} up -d dev worker
	@docker-compose ${ARGS} up --no-recreate --no-deps -d

serve:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Execute webpack serve command"
	@echo "------------------------------------------------------------------"
	@docker-compose ${ARGS} exec -T dev npm --prefix /home/web/django_project/frontend run serve
