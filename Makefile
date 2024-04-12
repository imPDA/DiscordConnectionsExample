DC = docker compose
APP_FILE = -f ./docker-compose/app.yaml
ENV_FILE = --env-file ./.env

build:
	${DC} ${APP_FILE} build
up:
	${DC} ${APP_FILE} ${ENV_FILE} up -d
	make logs-main
up-a:
	${DC} ${APP_FILE} ${ENV_FILE} up
logs:
	${DC} ${APP_FILE} logs --follow
logs-bot:
	${DC} ${APP_FILE} logs bot --follow
logs-main:
	${DC} ${APP_FILE} logs main-app --follow
down:
	${DC} ${APP_FILE} down
restart:
	make down
	make up
exec:
	docker exec -it ${APP_FILE} sh
