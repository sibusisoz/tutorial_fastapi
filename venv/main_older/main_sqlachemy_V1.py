from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg
from psycopg  import ClientCursor, ServerCursor 
from psycopg.rows import dict_row
import time
from . import models
from . import database
from . import schemas  
from . import utils
from .models import cUser,cPost
from .database import engine, SessionLocal
 
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
 
@app.get("/")
async def root():
    return {"message": "Sawubona Mhlaba!!!"}


@app.get("/posts",response_model=List[schemas.PostResp])
def get_posts(db: database.Session = Depends(database.get_db)):
    print("get all posts")  
    posts=db.query(models.cPost).all() 
    return posts
  
@app.get("/posts/{id}",response_model=schemas.PostResp)
def get_post(id: int,db: database.Session = Depends(database.get_db)): 
    print("get post by id ")   
    posts=db.query(models.cPost).filter(models.cPost.id == id).first()  
    
    if not posts:
        raise HTTPException(status_code=404, detail=f"post with id: {id} was not found")
    
    return posts

 
@app.post("/posts", status_code=status.HTTP_201_CREATED,response_model=schemas.PostResp)
def create_posts(npost: schemas.PostCreate,db: database.Session = Depends(database.get_db)):   
    print("ïnsert new post")   
    #print(','.join([f"{k}='{v}'" for k,v in npost.dict().items()]))
    posts=models.cPost(**npost.dict()) 
    
    db.add(posts)
    db.commit()
    db.refresh(posts) 
    return posts

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: database.Session = Depends(database.get_db)):  
    print("delete post")  
    posts=db.query(models.cPost).filter(models.cPost.id == id) 
    
    if not posts.first():
        raise HTTPException(status_code=404, detail=f"post with id: {id} was not found")
     
    posts.delete(synchronize_session=False) 
    db.commit()  
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}",response_model=schemas.PostResp)
def update_post(id: int, upost: schemas.PostCreate,db: database.Session = Depends(database.get_db)):   
    print("update post")  
    
    post_query=db.query(models.cPost).filter(models.cPost.id == id) 
    posts=post_query.first()
    
    if not posts:
       raise HTTPException (status_code= status.HTTP_404_NOT_FOUND,
                           detail = f'post with id : {id} does not exist')
 
    post_query.update(upost.dict(),synchronize_session=False) 
    db.commit()  
    return post_query.first()
 
@app.post("/users", status_code=status.HTTP_201_CREATED,response_model=schemas.UserResp)
def create_user(nuser: schemas.UserCreate,db: database.Session = Depends(database.get_db)):   
    print("ïnsert new user")   
     
    hashed_pw=utils.pw_hash(nuser.password) 
    nuser.password=hashed_pw
 
    new_user=models.cUser(**nuser.dict()) 
 
    db.add(new_user) 
    db.commit()
    db.refresh(new_user) 
    return   new_user
 
@app.get("/users/{id}", status_code=status.HTTP_201_CREATED,response_model=schemas.UserResp)
def get_user (id: int,db: database.Session = Depends(database.get_db)):   
    print("get user by id")       
    uUser=db.query(models.cUser).filter(models.cUser.id==id)
    print(uUser)
    print(id) 
    if not uUser.first()  :
        raise HTTPException(status_code=404, detail=f"user with id: {id} does not exist")
    
    return uUser.first()
     
     