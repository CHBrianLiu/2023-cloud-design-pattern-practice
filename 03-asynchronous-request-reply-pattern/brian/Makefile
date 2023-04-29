run-test:
	docker compose up -d --build
	docker compose exec webhook python -m unittest
	docker compose down
