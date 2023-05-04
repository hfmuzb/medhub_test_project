### Test assignment at medhub

Before starting the app, make sure ports 8000, 8001, 9000, 9001 are not being used already.
If these ports are in use by other apps, modify docker-compose.yml file, to use other ports.

To start the app with all the dependencies (database and minio) included, run these commands:

`make build`

`make run`

To run tests: 

`python3 -m venv .venv`

`cd <project-root>`

`pip install test_requirements.txt`

`make test`
