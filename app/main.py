from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    # healthcheck endpoint
    return {"message": "OK"}
