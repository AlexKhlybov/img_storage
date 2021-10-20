from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from .database import Base
# from routers.img_storage_api import get_db


class Inbox(Base):
    __tablename__ = 'inbox'

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String)
    name = Column(String, unique=True, index=True)
    create_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Inbox {self.name}>"

    def get_all_img(self):
        imgs = Inbox.query.all()
        results = [
            {'id': img.id, 'code': img.code, 'name': img.name, 'create_at': img.create_at} for img in imgs
        ]
        return results
    
    def create_img(self, data):
        img = Inbox(code=data.code, name=data.name)
        db = get_db()
        db.add(img)
        db.commit()

    def delete_img(self, id):
        img = Inbox.query.get_or_404(id)
        db = get_db()
        db.delete(img)
        db.commit()
