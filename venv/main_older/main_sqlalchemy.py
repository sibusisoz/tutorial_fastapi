from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg
from psycopg  import ClientCursor, ServerCursor 
from psycopg.rows import dict_row
import time
from . import models, database , schemas 
from .database import engine, SessionLocal


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#title str, content str are required
class Post(BaseModel):
   title: str
   content: str
   published: bool=True 
 
my_posts = [{"title": "foods","content":"plants","id":1},
            {"title": "drink","content":"tea","id":2},
            {"title": "dessert","content":"ice cream","id":3},
            {"title": "snack", "content": "crackers","id":4}, 
            {"title": "alcohol", "content": "whiskey","id":5},
            {"title": "test", "content": "testpost","id":6}
]

def find_post(id):
    for p in my_posts:
        print(p["id"])
        if p["id"] == id:
           return p 
              
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p["id"] == id:
           return i
       
def return_dict(stype):
    columns = [column[0] for column in cursor.description]
    #print(columns) 
    results = []
    
    if stype == "all":
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))  
    
    if stype == "one":
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))  
                         
    return results
   
@app.get("/")
async def root():
    return {"message": "Sawubona Mhlaba!!!"}


@app.get("/posts")
def get_posts(db: database.Session = Depends(database.get_db)):
    print("get all posts")  
    posts=db.query(models.cPost).all() 
    return {"data":posts}

@app.get("/posts/latest")
def get_latest_post(db: database.Session = Depends(database.get_db)): 
    print("cc") 
    #lpost=my_posts[len(my_posts)-1]
    return{"post detail": "cc"}
 
@app.get("/posts/{id}")
def get_post(id: int,db: database.Session = Depends(database.get_db)): 
    print("get post by id ")   
    npost=db.query(models.cPost).filter(models.cPost.id == id).first()  
    
    if not npost:
        raise HTTPException(status_code=404, detail=f"post with id: {id} was not found")
    
    return {"data": npost}

 
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(npost: Post,db: database.Session = Depends(database.get_db)):   
    print("ïnsert new post")   
    #print(','.join([f"{k}='{v}'" for k,v in npost.dict().items()]))
    nPost=models.cPost(**npost.dict()) 
    
    db.add(nPost)
    db.commit()
    db.refresh(nPost)
    
    return{"data": nPost}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: database.Session = Depends(database.get_db)):  
    print("delete post")  
    npost=db.query(models.cPost).filter(models.cPost.id == id) 
    
    if not npost.first():
        raise HTTPException(status_code=404, detail=f"post with id: {id} was not found")
     
    npost.delete(synchronize_session=False) 
    db.commit()  
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, upost: Post,db: database.Session = Depends(database.get_db)):   
    print("update post")  
    
    post_query=db.query(models.cPost).filter(models.cPost.id == id) 
    npost=post_query.first()
    
    if not npost:
       raise HTTPException (status_code= status.HTTP_404_NOT_FOUND,
                           detail = f'post with id : {id} does not exist')
 
    post_query.update(upost.dict(),synchronize_session=False) 
    db.commit()  
    return{"data":  post_query.first()}