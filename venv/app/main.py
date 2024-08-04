from fastapi import  FastAPI  
from .routers import user,post,auth,vote 
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

##comment out because we are using alembic
# from . import models
# from .database import engine
# models.Base.metadata.create_all(bind=engine)
 
app = FastAPI()
   
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "https://www.google.com/" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
app.include_router(post.router) 
app.include_router(user.router) 
app.include_router(auth.router) 
app.include_router(vote.router) 

@app.get("/")
async def root():
    return {"message": "Sawubona Mhlaba wethu!!!"}

# from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
# from fastapi.params import Body
# from pydantic import BaseModel
# from typing import Optional, List
# from random import randrange
# import psycopg
# from psycopg  import ClientCursor, ServerCursor 
# from psycopg.rows import dict_row
# import time
# from . import models, database, schemas, utils 
# from .database import engine, SessionLocal
# from .routers import user,post,auth
# models.Base.metadata.create_all(bind=engine)