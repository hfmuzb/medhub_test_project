sleep 3
cd app
alembic upgrade heads
uvicorn main:app --host 0.0.0.0 --port 8000
