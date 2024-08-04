from pydantic import BaseModel, EmailStr,ConfigDict, Field
from pydantic.types import conint
from datetime import datetime
from typing import  Optional, Annotated , List, Dict

#creating/sending class-to server
class PostBase(BaseModel):
        title: str
        content: str
        published: bool = True   

class PostCreate(PostBase):
        pass

class UserResp(BaseModel):
        id: int 
        email: EmailStr 
        created_at: datetime  

        model_config = ConfigDict(from_attributes=True) 
            
#response/results class-from server     
class PostResp(PostBase): 
        id: int
        created_at: datetime 
        owner_id: int
        owner: UserResp  

        model_config = ConfigDict(from_attributes=True)
        
class PostVotesResp(BaseModel):
        PostResp: PostResp 
        votes: int

        model_config = ConfigDict(from_attributes=True) 
         
class PostVoteResp(PostBase): 
        id: int
        created_at: datetime 
        owner_id: int   
        email: EmailStr 
        votes: int

        model_config = ConfigDict(from_attributes=True)
         
        
#creating/sending class-to server            
class UserCreate(BaseModel):
        email: EmailStr
        password: str  
        
class UserLogin(BaseModel):
        email: EmailStr
        password: str  
 
class Token(BaseModel):
        access_token: str
        token_type: str 
        
class TokenData(BaseModel):
        id: Optional[str] = None
 
class Vote(BaseModel):
        post_id: int
        dir: Annotated[int, Field(strict=True,gt=-1, le=1)] 