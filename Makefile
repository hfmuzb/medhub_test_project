run:
	docker compose up -d app minio db

build:
	docker compose build app

stop:
	docker compose down


restart:
	docker compose down
	docker compose build app
	docker compose up -d app minio db
