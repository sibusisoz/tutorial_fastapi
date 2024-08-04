from fastapi import HTTPException, Depends, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from .. import models, database, schemas, utils,oauth2

router= APIRouter( tags=["Authentication"]) 

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: database.Session = Depends(database.get_db)):
    print("user login")       
    uUser=db.query(models.cUser).filter(models.cUser.email==user_credentials.username).first()
    print(uUser)  
     
    if not uUser :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    validate=utils.verify_hash(user_credentials.password, uUser.password)
    if not validate:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
     
    #create a token 
    access_token=oauth2.create_access_token(data={"user_id":uUser.id})
  
    return {"access_token": access_token, "token_type":"bearer"}