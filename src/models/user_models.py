from sqlalchemy import Column, String, Integer
from config.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username:str=Column(String, unique=True, nullable=False)
    email:str=Column(String)
    hashed_password:str=Column(String,unique=False,nullable=False)
    image_url:str=Column(String,nullable=True)
