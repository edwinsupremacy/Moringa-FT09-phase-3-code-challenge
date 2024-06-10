from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Magazine(Base):
    __tablename__ = 'magazines'

    id=Column(Integer,primary_key=True)
    _name = Column(String, nullable=False)
    category = Column(String, nullable=False)

    articles = relationship("Article", back_populates="magazine")

    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category
    
    @property
    def id(self):
        return self.id

    @id.setter
    def id(self,id):
        if not isinstance(id,int):
            raise ValueError ("Id should be a number")
      

    @property
    def name(self):
        return self.name

    @name.setter
    def name(self,name):
        if not isinstance(name,str):
            raise ValueError("Not a string")
        if not (2<= len(name)<=16):
            raise ValueError("Exceeded character limit");
    
        
    def __repr__(self):
        return f'<Magazine {self.name}>'
