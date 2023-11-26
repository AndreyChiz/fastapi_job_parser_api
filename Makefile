.PHONY: clean
.PHONY: run

clean:
	docker-compose down --rmi all
run:
	docker-compose up -d --build

