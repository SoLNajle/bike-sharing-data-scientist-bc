#

ps: status

status: 
	@docker-compose ps

start:
	@docker-compose up -d

stop:
	@docker-compose down

kill:
	@docker-compose kill
	@docker-compose rm -f
