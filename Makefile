DC = docker compose
APP_FILE = -f ./docker-compose/app.yaml
BROKER_FILE = -f ./docker-compose/broker.yaml
ENV_FILE = --env-file ./.env

ALL_FILES = ${APP_FILE} ${BROKER_FILE}

build:
	${DC} ${ALL_FILES} build
up:
	${DC} ${ALL_FILES} ${ENV_FILE} up -d
	make logs-main
up-a:
	${DC} ${ALL_FILES} ${ENV_FILE} up
logs:
	${DC} ${ALL_FILES} logs --follow
logs-bot:
	${DC} ${ALL_FILES} logs bot --follow
logs-main:
	${DC} ${ALL_FILES} logs main-app --follow
down:
	${DC} ${ALL_FILES} down
restart:
	make down
	make up
exec:
	docker exec -it ${ALL_FILES} sh
