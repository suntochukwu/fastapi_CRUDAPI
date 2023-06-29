from jose import JWTError, jwt
from datetime import datetime, timedelta
from app import schemas,database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer 
from sqlalchemy.orm import session

oath2scheme= OAuth2PasswordBearer(tokenUrl='login')

#secretkey
#algorithm
#expirationtime

secretkey = "asdsgsddg435346dfghdf95675"
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES=30

def create_access_token(data: dict):
    to_encode=data.copy()
    expire= datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt= jwt.encode(to_encode, secretkey,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credential_exception):
    try:
        payload=jwt.decode(token, secretkey,algorithms=[ALGORITHM])
        id : str = payload.get('user_id')
        if id is None:
            raise credential_exception
        token_data= schemas.TokenData(id=id)
    except JWTError:
        raise credential_exception
    return token_data

def get_current_user(token: str = Depends(oath2scheme), db : session=Depends(database.get_db )):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
    detail= "could not validate credentials", headers={"www-authenticate":"bearer"})
    
    token=  verify_access_token(token, credentials_exception)   
    user= db.query(models.users).filter(models.users.id == token.id).first()
    return user