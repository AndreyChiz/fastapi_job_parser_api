.PHONY: clean
.PHONY: run
.PHONY: stop


clean:
	docker-compose down --rmi all


run:
	docker-compose up -d

stop:
	docker-compose stop