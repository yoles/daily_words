COMPOSE=local.yml
FIG=docker-compose -f $(COMPOSE)
PROJECT_NAME=$(shell basename $(shell pwd))
HEROKU_NAME=lion-bot-backend
REGISTRY_NAME=registry.heroku.com
RUN=$(FIG) run --rm
SERVICE=backend
SERVICE_DB=db
EXEC=$(FIG) exec
BACKUP_SQL=backup.sql
TMP_SQL=tmp.sql
MANAGE=python manage.py
# setaf: set foreground color
RED:=$(shell tput setaf 1)
YELLOW:=$(shell tput setaf 3)
COLOR_RESET:=$(shell tput sgr0)


.DEFAULT_GOAL := help
.PHONY: help start stop poetry
.PHONY: build up down

help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

##
## Project setup
##---------------------------------------------------------------------------

start:          ## Install and start the project
start: build up


##
## Command
##---------------------------------------------------------------------------

showcommand:	## show all personnal command
showcommand:
	$(RUN) $(SERVICE) $(MANAGE)

executecommand: ## usage: name=[command]
executecommand:
	$(RUN) $(SERVICE) $(MANAGE) $(name)


##
## Internal rules
##---------------------------------------------------------------------------

build:
	$(FIG) build

up:	## Start project container
	$(FIG) up

down: ## Stop project container
	$(FIG) down

plain-app:   ## make django app name=[name]
plain-app:
	$(EXEC) $(SERVICE) bash -c "cd apps && django-admin startapp $(name)"

term-app:	## make django app with user right appname=[name]
term-app: plain-app
	sudo chown -R ${USER}:${USER} ./apps/$(name)
	$(info $(YELLOW)Don't forget to add $(name) into api/setting/base.py$(COLOR_RESET))

container-shell:	## Start container
container-shell:
	$(EXEC) -it $(SERVICE)


project:	## Make django project with apps and data folders
project:
	$(RUN) $(SERVICE) django-admin startproject $(PROJECT_NAME) .
	mkdir apps


permissions:	## Give current user right on project
permissions:
	sudo chown -R ${USER}:${USER} ./

hosts:	## Allowed Host: Copy / Paste this line on init project
hosts:
	sed -i '0,/ALLOWED_HOSTS = \[\]/s//ALLOWED_HOSTS = [\"0.0.0.0\", \"127.0.0.1\", \"localhost\"]/' ./$(PROJECT_NAME)/settings.py

db-dump:
	$(EXEC) $(SERVICE_DB) bash -c "pg_dumpall -U postgres > backup.sql"
	docker cp $(shell docker ps --no-trunc -aqf name=a$(PROJECT_NAME)_db):/$(BACKUP_SQL) $(TMP_SQL)
	sed '/CREATE ROLE postgres;/d' ./$(TMP_SQL) > $(BACKUP_SQL)
	rm $(TMP_SQL)

force-clean:
	docker container prune
	docker image prune
	docker rmi -f $(PROJECT_NAME)_backend postgres $(PROJECT_NAME)_db
	docker ps
	docker ps -a
	docker images

force-restart:	## removes images and container, rebuild, and start project
force-restart: force-clean start

connect-db:
connect-db:
	docker exec -it $(shell docker ps --no-trunc -aqf name=$(PROJECT_NAME)_db) bash

##
## In Container
##---------------------------------------------------------------------------

# https://www.gnu.org/software/make/manual/make.html#Make-Control-Functions
app:	## make django app with user right appname=[name]
app:
	cd ./apps && django-admin startapp $(name)
	$(info $(YELLOW)Don't forget to add $(name) into api/setting/base.py$(COLOR_RESET))

color-test:

shell:	## run shell from inside a container
shell:
	$(MANAGE) shell

migrations-app:	## makemigrations for an app name=<>
migrations-app:
	$(MANAGE) makemigrations $(name)


migrate-app:	## migrate for an app name=<>
migrate-app:
	$(MANAGE) migrate $(name)


makemigrate-app:	## Do makemigrations and migrate for an app appname=<>
makemigrate-app: migrations-app migrate-app


makemigrate-project: ## Do makemigrations and migrate for an app appname=<>
makemigrate-project:
	$(MANAGE) makemigrations
	$(MANAGE) migrate


test-path: ## Generate test path for a given file
test-path:
	@echo $(shell echo $(path) | sed 's/\//./g' | head -c-4)

write-zsh:
	@echo 'alias get_path="python /app/path_2_test.py"' >> ~/.zshrc
	$(info $(YELLOW)Don't forget to execute: source ~/.zshrc$(COLOR_RESET))

write-bashrc:
	@echo 'alias get_path="python /app/path_2_test.py"' >> ~/.bashrc
	$(shell source ~/.bashrc)

init:
	sudo chmod +x ./init.sh
	./init.sh $(PROJECT_NAME)

remove-images:
	docker container prune
	docker rmi -f $(shell docker images --no-trunc -aq $(PROJECT_NAME)_db) $(shell docker images --no-trunc -aq $(PROJECT_NAME)_backend)

remove: remove-images
	make permissions
	rm -Rf ../$(PROJECT_NAME) && cd ..


install:
	pip install -r requirements/dev.txt

translate:
	$(MANAGE) makemessages -l fr
	$(MANAGE) compilemessages

##
## Unit Testing
##--------------------------
run-cov:
	coverage run manage.py test apps

run-cov-report: run-cov
	coverage report -m

run-cov-xml: run-cov
	coverage xml


# Stripes
stripe-webhook:
	stripe listen --forward-to localhost:8000/api/v1/subscription/webhook/

##
## Unit Testing
##--------------------------

heroku-login:
	heroku container:login

heroku-create:
	heroku create -a $(HEROKU_NAME) --buildpack heroku/python --region eu

heroku-create-db:
	heroku addons:create heroku-postgresql:hobby-dev -a $(HEROKU_NAME)

heroku-migrate:
	heroku run python manage.py makemigrations -a $(HEROKU_NAME)
	heroku run python manage.py migrate -a $(HEROKU_NAME)

heroku-rmimage:
	docker rmi -f  $(shell docker images --no-trunc -aq $(REGISTRY_NAME)/$(HEROKU_NAME)/web)

heroku-build:
	docker build -f DockerfileProd -t $(REGISTRY_NAME)/$(HEROKU_NAME)/web .
	docker push $(REGISTRY_NAME)/$(HEROKU_NAME)/web
	heroku container:release -a $(HEROKU_NAME) web

heroku-init: heroku-create heroku-create-db heroku-build

heroku-deploy: heroku-rmimage heroku-build

heroku-shell:
	heroku run sh -a $(HEROKU_NAME)
