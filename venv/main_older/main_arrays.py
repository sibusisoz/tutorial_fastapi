from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

#title str, content str are required
class Post(BaseModel):
   title: str
   content: str
   published: bool=True
   rating: Optional[int]=None

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
       
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():

    return{"posts": my_posts}
''' 
@app.post("/createposts")
def create_posts(payload: dict=Body(...)):
    print(payload)
    return{"new_post": f"title {payload['title']} content: {payload['content']} "}
'''
@app.post("/posts", status_code=status.HTTP_201_CREATED)
#@app.post("/posts")
def create_posts(npost: Post): 
    n_post=npost.dict()
    n_post["ïd"]=randrange(0,10000)
    my_posts.append(n_post) 
    return{"_post": n_post}
    #return{"new_post": f"title {payload['title']} content: {payload['content']} "}
    #return{"new_post": f"title: {npost.title} content: {npost.content}"}
 
@app.get("/posts/latest")
def get_latest_post(): 
    lpost=my_posts[len(my_posts)-1]
    return{"post detail": lpost}
  
@app.get("/posts/{id}")
def get_post(id: int): 
#def get_post(id: int,rpost: Response): 
    gpost=find_post(id) 
    if not gpost:
        raise HTTPException(status_code=404, detail=f"post with id: {id} was not found")
        #rpost.status_code=status.HTTP_404_NOT_FOUND 
        #return {"message": f" post with id: {id} was not found"}     
    return{"post detail": gpost}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):  
    ipos=find_index_post(id) 
    if ipos == None:
        raise HTTPException(status_code=404, detail=f"post with id: {id} was not found")
    my_posts.pop(ipos)     
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, upost: Post):  
    print("inupdate")
    ipos=find_index_post(id) 
   
    if ipos == None:
        raise HTTPException(status_code=404, detail=f"post with id: {id} was not found")
    
    npost=upost.dict()    
    npost["id"] =id
    my_posts[ipos]=npost
    return{"data": npost}