from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import os
print (os.getcwd())

from models.database import SessionLocal
from models.inbox import Inbox

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import uuid

templates = Jinja2Templates(directory="templates")
app = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/frame/")
async def get_home(request: Request, db: Session = Depends(get_db)):
    data = {'say': 'WFT'}
    return templates.TemplateResponse("index.html", {"request": request, 'data': data})


@app.post("/frame/")
async def create_upload_file(file: UploadFile = File(...)):
    
    file.filename = f"data/{uuid.uuid4()}.jpg"
    contents = await file.read()

    with open(file.filename, "wb") as f:
        f.write(contents)
    


    return {"filename": file.filename}

@app.get("/frame/")
async def get_home(request: Request, db: Session = Depends(get_db)):
    data = {'say': 'WFT'}
    return templates.TemplateResponse("index.html", {"request": request, 'data': data})


# @app.put("/frame/{frame_id}", status_code=202, responses={**responses})
# def town_update(town_id: int, data: TownModel, db: Session = Depends(get_db)):
#     town = get_town(db=db, town_id=town_id)
#     if town is None:
#         raise HTTPException(status_code=404, detail="Town not found!")
#     else:
#         return update_town(db=db, town_id=town_id, data=data)


# @app.delete("/frame/{frame_id}", responses={**responses}, status_code=202)
# def town_delete(town_id: int, db: Session = Depends(get_db)):
#     town = get_town(db=db, town_id=town_id)
#     if town is None:
#         raise HTTPException(status_code=404, detail="Town not found!")
#     else:
#         delete_town(db=db, town_id=town_id)


# @app.post("/api/town/", status_code=201)
# async def town_create(town: TownModel, db: Session = Depends(get_db)):
#     town_el = create_town(db=db, data=town)
#     town_aw = await get_weater(db=db, item=town_el)
#     return town_aw.get_dict