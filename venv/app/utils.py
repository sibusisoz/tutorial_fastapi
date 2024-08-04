
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 

def pw_hash (passwd: str):
    return  pwd_context.hash(passwd)

def verify_hash (plainpasswd,hashpasswd):
    return  pwd_context.verify(plainpasswd,hashpasswd)