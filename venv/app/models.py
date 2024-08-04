from sqlalchemy import Column, Integer,String,Boolean,ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship  
from .database import Base

class cPost(Base):
    __tablename__ = "tposts"

    id = Column(Integer, primary_key=True,nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("tusers.id",ondelete="Cascade"), nullable=False)
    
    owner = relationship("cUser")

class cUser(Base):
    __tablename__ = "tusers"

    id = Column(Integer, primary_key=True,nullable=False)
    email = Column(String, nullable=False,unique=True)
    password = Column(String, nullable=False) 
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,server_default=text('now()'))
    phone_number = Column(String, nullable=True) 
 
class cVote(Base):
    __tablename__ = "tvotes"
    user_id = Column(Integer, ForeignKey("tusers.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("tposts.id", ondelete="CASCADE"), primary_key=True)