## Test assignment at medhub

Before starting the app, make sure ports `8000`, `8001`, `9000`, `9001` are not being used already.
If these ports are in use by other apps, modify docker-compose.yml file, to use other ports.

### To start the app with all the dependencies (database and minio) included, run these commands:

- `make build`

- `make run`
- after visit http://localhost:8000/docs to view the swagger docs and manually test available endpoints

### To run tests: 

Create and activate virtual environment:
- `python3 -m venv .venv`

- `source .venv/bin/activate`
- `cd <project-root>`

Install requirements: 
- `pip install -r test_requirements.txt`

Run postgres and minio containers, which are used by the app:
- `docker compose up -d minio db`

Apply migrations:
- `cd app`

- `alembic upgrade heads`

Go to project root dir, and run tests
- `cd ..`
- `pytest tests`

Stop postgres and minio containers:
- `docker compose down`
