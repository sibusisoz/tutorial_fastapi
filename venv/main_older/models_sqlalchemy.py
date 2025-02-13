from email.policy import default
from enum import unique
from sqlalchemy import Column, Integer,String,Boolean 
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database_sqlalchemy import Base

class cPost(Base):
    __tablename__ = "tposts"

    id = Column(Integer, primary_key=True,nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,server_default=text('now()'))

class cUser(Base):
    __tablename__ = "tusers"

    id = Column(Integer, primary_key=True,nullable=False)
    email = Column(String, nullable=False,unique=True)
    password = Column(String, nullable=False) 
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,server_default=text('now()'))