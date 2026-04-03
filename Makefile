SHELL := /bin/bash

.PHONY: up down restart logs check ps clean

up:
	./scripts/up.sh

down:
	./scripts/down.sh

restart:
	./scripts/down.sh
	./scripts/up.sh

logs:
	docker compose logs -f

check:
	./scripts/check.sh

ps:
	docker compose ps

clean:
	docker compose down -v