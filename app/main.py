from fastapi import FastAPI

from routers.patients import router as patient_routers
from service.storage import s3
from config import config

app = FastAPI()
app.include_router(patient_routers)


@app.on_event("startup")
async def startup_event():
    # try to create minio bucket
    await s3.create_bucket(bucket=config.MINIO_BUCKET)


@app.get("/")
async def root():
    # healthcheck endpoint
    return {"message": "OK"}
