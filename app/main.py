from fastapi import FastAPI

from routers.patients import router as patient_routers

app = FastAPI()
app.include_router(patient_routers)


@app.get("/")
async def root():
    # healthcheck endpoint
    return {"message": "OK"}
