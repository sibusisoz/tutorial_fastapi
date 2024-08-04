from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
import json
from json  import JSONEncoder
from .. import schemas, database, models, oauth2
from sqlalchemy.sql import func 
from typing import List, Optional
from dataclasses import dataclass

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

 

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(nvote: schemas.Vote, db: database.Session = Depends(database.get_db),current_user: int =Depends(oauth2.get_current_user)):
       
    post_query= db.query(models.cPost).filter(models.cPost.id == nvote.post_id)
    post=post_query.first()
  
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {nvote.post_id} does not exist")

    vote_query = db.query(models.cVote).filter(models.cVote.post_id == nvote.post_id,
                                              models.cVote.user_id == current_user.id)

    found_vote = vote_query.first()
    print(vote_query)
    print(found_vote) 
    if (nvote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has alredy voted on post {nvote.post_id}")
        new_vote = models.cVote(post_id=nvote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()

    return {"message": "successfully deleted vote"}
 
@router.get("/voted/" ,response_model=List[schemas.PostVoteResp])
def get_votes(db: database.Session = Depends(database.get_db),current_user: int =Depends(oauth2.get_current_user)):
    print("get all posts")     
    print(current_user.email)
        
    #vote_query = db.query(models.cPost, func.count(models.cVote.post_id).label("votes")).join(models.cVote, models.cVote.post_id == models.cPost.id, isouter=True).group_by(models.cPost.id)
    #vote_query = db.query(models.cPost).join(models.cVote, models.cVote.post_id == models.cPost.id, isouter=True).group_by(models.cPost.id)
    
    vote_query = db.query(models.cPost.id,models.cPost.title,models.cPost.content,models.cPost.created_at,models.cPost.owner_id,models.cUser.email,
                          func.count(models.cVote.post_id).label("votes")
                          ).join(models.cVote, models.cVote.post_id == models.cPost.id, isouter=True
                          ).join(models.cUser, models.cUser.id == models.cPost.owner_id, isouter=True
                          ).group_by(models.cPost.id,models.cUser.id )
    #SELECT tposts.id AS tposts_id, tposts.title AS tposts_title, tposts.content AS tposts_content, tposts.published AS tposts_published, tposts.created_at AS tposts_created_at, tposts.owner_id AS tposts_owner_id, count(tvotes.post_id) AS votes
     
    print(vote_query) 
     
    v_query = vote_query.all()
    #for result in vote_query: 
        #print(result) 
   
    return v_query  
  