import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers import img_storage_api as routers
from models.inbox import Base
from models.database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(routers.app)

app.mount("/data", StaticFiles(directory="data"), name="data")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    