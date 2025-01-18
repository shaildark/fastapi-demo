from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    iRoleId = Column(Integer, default=1)
    vUserName = Column(String(150))
    vFirstName = Column(String(150))
    vLastName = Column(String(150))
    email = Column(String(255))
    password = Column(String(255))
    vProfileImage = Column(String(255))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, default=None)

    @classmethod
    def query(cls, session: sessionmaker):
        return session.query(cls).filter(cls.deleted_at == None)

    @classmethod
    def get_by_email(cls, session: sessionmaker, email: str):
        return session.query(cls).filter(cls.email == email).first()
    
    @classmethod
    def get_by_id(cls, session: sessionmaker, id: int):
        return session.query(cls).filter(cls.id == id).first()