from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from core.models import db_helper
from api.api_v1.coordinates import router as coordinates_router


@asynccontextmanager
async def lifespan(app: FastAPI):  # type: ignore
    # startup
    yield
    # shutdown
    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def hello_wrld() -> dict:
    return {
        "message": "Hello, my friend, use /docs after url for better testing this app"
    }
app.include_router(coordinates_router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
