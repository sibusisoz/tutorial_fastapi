from fastapi import Body, FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg
from psycopg  import ClientCursor, ServerCursor 
from psycopg.rows import dict_row
import time
    
app = FastAPI()

#title str, content str are required
class Post(BaseModel):
   title: str
   content: str
   published: bool=True 

try:
    #conn = psycopg.connect(host="localhost",database=fastapi,user="postgres",
    #                       password="Mcdaddy1")
    conn = psycopg.connect("dbname=fastapi user=postgres",password="Mcdaddy1", host="localhost",cursor_factory=ClientCursor)
    cursor= conn.cursor()
    print("Database connection was succesfull")
except Exception as error:
    print("Connection to DB failed") 
    print("Error: ", error)
    time.sleep(2)   

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
  
@app.get("/posts/latest")
def get_latest_post(): 
    print("cc") 
    #lpost=my_posts[len(my_posts)-1]
    return{"post detail": "cc"}
 
@app.get("/posts/{id}")
def get_post(id: int): 
    #gposts=return_dict()
    cursor.execute("""select * from tposts where id = %s """,(str(id),)) 
    gpost=return_dict("one") 
    if not gpost:
        raise HTTPException(status_code=404, detail=f"post with id: {id} was not found")
    return{"post detail": gpost}

@app.get("/posts")
def get_posts():
    print("get all posts")  
    cursor.execute("""select * from tposts""") 
    gposts=return_dict("all")
    return{"posts": gposts}
 
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(npost: Post):   
    print("ïnsert new post")  
    cursor.execute("""INSERT INTO tposts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(npost.title,npost.content,npost.published) )
    gposts=return_dict("one") 
    conn.commit()
    return{"data": gposts}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):  
    print("delete post")  
    cursor.execute("""delete from tposts where id = %s  RETURNING * """,(str(id),)) 
    gpost=return_dict("one")
    print (id)  
    conn.commit() 
    if not gpost:
        raise HTTPException(status_code=404, detail=f"post with id: {id} was not found")
       
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, upost: Post):   
    print("update post")  
    update_query = """
        UPDATE tposts
        SET 
         (title, content, published)
          =
         (%s, %s, %s)
        WHERE id= (%s)   RETURNING * """ 
        
    cursor.execute(update_query, (upost.title,upost.content,upost.published,str(id))) 
    #cursor.execute("""UPDATE tposts SET title=%s, content=%s, published=%s WHERE id = %s returning * """, 
    #(npost.title,npost.content,npost.published,str(id))) 
    gpost=return_dict("one") 
    conn.commit()   
    if not gpost:
     raise HTTPException (status_code= status.HTTP_404_NOT_FOUND,
                           detail = f'post with id : {id} does not exist')
    
    return{"data": gpost}