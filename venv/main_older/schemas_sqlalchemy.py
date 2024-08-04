from pydantic import BaseModel

#title str, content str are required
class Post(BaseModel):
   title: str
   content: str
   published: bool=True 