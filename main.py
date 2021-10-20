import uvicorn
from fastapi import FastAPI

from routers import img_storage_api as routers
from models.inbox import Inbox, Base
from models.database import SessionLocal, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(routers.app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    