import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from models.database import engine
from models.inbox import Base
from routers import img_storage_api as routers

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(routers.app)

app.mount("/upload_data", StaticFiles(directory="upload_data"), name="upload_data")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    