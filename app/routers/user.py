
from .. import models,schemas, utils
from fastapi import Body, Depends, FastAPI, Response,status, HTTPException, APIRouter
from ..database import engine , get_db
from sqlalchemy.orm import session 


router= APIRouter(
    prefix='/users',
    tags=['Users']

)
@router.post("/",status_code=status.HTTP_201_CREATED, response_model= schemas.UserOut)
def create_user(user: schemas.UserCreate ,db: session = Depends (get_db)):
    hashed_password= utils.hash(user.password)
    user.password=hashed_password
    new_user = models.users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}',status_code=status.HTTP_200_OK, response_model= schemas.UserOut)
def get_user(id:int,db: session = Depends (get_db)):
    user_found= db.query(models.users).filter(models.users.id==id).first()
    if not user_found:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail = f"user with id {id} not found")
    return user_found
