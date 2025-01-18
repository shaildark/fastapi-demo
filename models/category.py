from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from .database import Base 

class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    vName = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, default=None)

    products = relationship("Product", back_populates="category", lazy="joined")

    def __repr__(self):
        return f"<Category(id={self.id}, vName='{self.vName}')>"

    @classmethod
    def query(cls, session: sessionmaker):
        return session.query(cls).filter(cls.deleted_at == None)
    
    @classmethod
    def get_by_id(cls, session: sessionmaker, id: int):
        return session.query(cls).filter(cls.id == id).first()

    @classmethod
    def get_by_name(cls, session: sessionmaker, name: str):
        return session.query(cls).filter(cls.vName == name).first()