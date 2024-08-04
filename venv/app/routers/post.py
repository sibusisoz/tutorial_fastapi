from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, database, schemas,oauth2
from typing import List, Optional

router= APIRouter(
            prefix="/posts", 
            tags=["Posts"]) 

@router.get("/",response_model=List[schemas.PostResp])
def get_posts(db: database.Session = Depends(database.get_db),current_user: int =Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = "" ):
    print("get all posts")     
    print(current_user.email)
    # original query
    posts=db.query(models.cPost).all() 
    print("xxxx") 
    print(posts) 
    print("xxxx")
    #- paginationlimit=query parameter, limit number of posts returned. Spik first number of records=Offset, search key words 
    posts=db.query(models.cPost).filter(models.cPost.title.contains(search)).limit(limit).offset(skip).all() 
    
    print(posts) 
    #limit to owners post only
    #posts=db.query(models.cPost).filter(models.cPost.owner_id==current_user.id).all() 
 
    return posts
     
  
@router.get("/{id}",response_model=schemas.PostResp)
def get_post(id: int,db: database.Session = Depends(database.get_db),current_user: int =Depends(oauth2.get_current_user)): 
    print("get post by id ")   
    posts=db.query(models.cPost).filter(models.cPost.id == id).first()  
    
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    #limit to owners post only 
    # if posts.owner_id !=current_user.id:
    #      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorised to perform requested action")
    
    return posts

 
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.PostResp)
def create_posts(npost: schemas.PostCreate,db: database.Session = Depends(database.get_db),current_user: int =Depends(oauth2.get_current_user)):   
    print("ïnsert new post")   
    print(current_user.email)
    posts = models.cPost(owner_id=current_user.id, **npost.dict())
    db.add(posts)
    db.commit()
    db.refresh(posts) 
    return posts

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: database.Session = Depends(database.get_db),current_user: int =Depends(oauth2.get_current_user)):  
    print("delete post")  
    
    post_query=db.query(models.cPost).filter(models.cPost.id == id) 
    posts=post_query.first()
     
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
 
    
    if posts.owner_id !=current_user.id:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorised to perform requested action")
   
    post_query.delete(synchronize_session=False) 
    db.commit()  
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model=schemas.PostResp)
def update_post(id: int, upost: schemas.PostCreate,db: database.Session = Depends(database.get_db),current_user: int =Depends(oauth2.get_current_user)):   
    print("update post")  
    
    post_query=db.query(models.cPost).filter(models.cPost.id == id) 
    posts=post_query.first()
    
    if not posts:
       raise HTTPException (status_code= status.HTTP_404_NOT_FOUND,
                           detail = f'post with id : {id} does not exist')
 
    if posts.owner_id !=current_user.id:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorised to perform requested action")
    
    post_query.update(upost.dict(),synchronize_session=False) 
    db.commit()  
    return post_query.first()
 