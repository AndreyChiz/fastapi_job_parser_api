.PHONY: clean
.PHONY: run
.PHONY: stop


clean:
	docker-compose down --rmi all


run:
	docker-compose up -d --build

stop:
	docker-compose stop