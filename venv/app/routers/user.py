from fastapi import   status, HTTPException, Depends, APIRouter
from .. import models, database, schemas, utils  
 
router= APIRouter(
               prefix="/users",
               tags=["Users"]) 
 
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.UserResp)
def create_user(nuser: schemas.UserCreate,db: database.Session = Depends(database.get_db)):   
    print("ïnsert new user")   
     
    hashed_pw=utils.pw_hash(nuser.password) 
    nuser.password=hashed_pw
 
    new_user=models.cUser(**nuser.dict()) 
 
    db.add(new_user) 
    db.commit()
    db.refresh(new_user) 
    return   new_user
 
 
 
@router.get("/{id}", status_code=status.HTTP_201_CREATED,response_model=schemas.UserResp)
def get_user (id: int,db: database.Session = Depends(database.get_db)):   
    print("get user by id")       
    uUser=db.query(models.cUser).filter(models.cUser.id==id)
    print(uUser)
    print(id) 
    if not uUser.first()  :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist")
    
    return uUser.first()
     
     