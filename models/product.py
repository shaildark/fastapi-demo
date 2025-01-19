from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from .database import Base

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, autoincrement=True)
    iCategoryId = Column(Integer, ForeignKey("category.id"), nullable=True)
    vName = Column(String(255), nullable=True)
    fPrice = Column(Float(10, 6), nullable=True)
    tDescription = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, default=None)

    category = relationship("Category", back_populates="products", lazy="joined")

    def __repr__(self):
        return f"<Product(id={self.id}, vName='{self.vName}', fPrice={self.fPrice})>"
    
    @classmethod
    def query(cls, session: sessionmaker):
        return session.query(cls).filter(cls.deleted_at == None)
    
    @classmethod
    def get_by_id(cls, session: sessionmaker, id: int, category_id: int = None):
        query = cls.query(session).filter(cls.id == id)
        if category_id is not None:
            query = query.filter(cls.iCategoryId == category_id)

        return query.first()
    
    @classmethod
    def get_by_name(cls, session: sessionmaker, name: str, category_id: int = None):
        query = cls.query(session).filter(cls.vName == name)
        if category_id is not None:
            query = query.filter(cls.iCategoryId == category_id)
        
        return query.first()