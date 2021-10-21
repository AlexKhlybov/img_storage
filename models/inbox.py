from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import Session

from .database import Base


class Inbox(Base):
    __tablename__ = 'inbox'

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String)
    name = Column(String, unique=True, index=True)
    create_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Inbox {self.name}>"

    @staticmethod
    def get_dict(obj):
        return {
            'id': obj.id,
            'code': obj.code,
            'name': obj.name,
            'create_at': obj.create_at
            }

    @staticmethod
    def get_img(db: Session, img_id: int):
        img = db.query(Inbox).filter(Inbox.id == img_id).first()
        if img:
            return img
        return None

    @staticmethod
    def get_all_img(db: Session):
        imgs = db.query(Inbox).all()
        results = [Inbox.get_dict(img) for img in imgs]
        return results
    
    @staticmethod
    def create_img(db: Session, data):
        img = Inbox(code=data['code'], name=data['filename'])
        db.add(img)
        db.commit()

    @staticmethod
    def delete_img(db: Session, img_id: int):
        img = db.query(Inbox).get(img_id)
        db.delete(img)
        db.commit()
