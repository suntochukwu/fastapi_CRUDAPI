from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import session 
from .. import models, database, schemas, utils, oath2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from fastapi.security import OAuth2PasswordBearer


router= APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends( ), db: session=Depends(database.get_db)):
    user = db.query(models.users).filter(models.users.email== user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail = "invalid credentials")
    
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "invalid credentials")
    #create token
    access_token=oath2.create_access_token(data={"user_id":user.id})
    return {"access token": access_token, "token type": "bearer"}

