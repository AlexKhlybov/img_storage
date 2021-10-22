import os
import uuid
from datetime import datetime
from typing import List

from fastapi import (APIRouter, Depends, File, HTTPException, Request,
                     UploadFile)
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from models.database import SessionLocal, get_db
from models.inbox import Inbox

templates = Jinja2Templates(directory="templates")
app = APIRouter()


def delete_file(obj):
    folder = ''.join((str(obj.create_at).split(' '))[0].split('-'))
    cur_dir = os.path.join(os.getcwd(), f'upload_data/{folder}/')

    while True:
        file_list = os.listdir(cur_dir)
        if obj.name in file_list:    
            os.remove(os.path.join(cur_dir, obj.name))
            break
    if not len(os.listdir(cur_dir)):
        os.rmdir(cur_dir)


@app.get("/frame/", 
        responses={
            200: {
                "description": "OK!",
                "content": {
                    "application/json": {
                        "example": [
                            {
                                "id": 1,
                                "code": "string",
                                "...": "...",
                            },
                            {
                                "id": 2,
                                "code": "string",
                                "...": "...",
                            },
                        ]
                    }
                },
            },
        },
    )
async def get_list_img(db: Session = Depends(get_db)):
    img = Inbox.get_all_img(db=db)
    return img


@app.put("/frame/", 
        responses={
            201: {
                "description": "OK!",
                "content": {
                    "application/json": {
                        "example": [
                            {
                                "id": 8,
                                "code": "string",
                                "...": "...",
                            },
                            {
                                "id": 7,
                                "code": "string",
                                "...": "...",
                            },
                        ]
                    }
                },
            },
        },
    )
async def upload_file(request: Request, up_file: List[UploadFile] = File(...),
                             db: Session = Depends(get_db)):
    
    str_date = datetime.today().strftime('%Y%m%d')
    if len(up_file) > 15:
        raise HTTPException(status_code=400, detail="Не могу за раз больше 15!")

    if not os.path.exists(f'upload_data/{str_date}'):
        os.mkdir(f'upload_data/{str_date}')

    for file in up_file:
        file.filename = f"{uuid.uuid4()}.jpg"
        path = f"upload_data/{str_date}/{file.filename}"
        contents = await file.read()
        with open(path, "wb") as f:
            f.write(contents)
        data = {
            'code': request.url.path,
            'filename': file.filename
            }
        Inbox.create_img(db=db, data=data)
    return {'detail': 'Files uploaded successfully!'}


@app.delete("/frame/{img_id}", status_code=202)
async def delete_img(img_id: int, db: Session = Depends(get_db)):
        img = Inbox.get_img(db=db, img_id=img_id)
        if img is None:
            raise HTTPException(status_code=404, detail="Image not found!")
        else:
            Inbox.delete_img(db=db, img_id=img_id)
            delete_file(img)
            return {'detail': 'Files delete successfully!'}
        
        
