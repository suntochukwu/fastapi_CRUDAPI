

from .. import models,schemas,oath2
from fastapi import Body, Depends, FastAPI, Response,status, HTTPException, APIRouter
from ..database import engine , get_db
from sqlalchemy.orm import session 
from typing import List, Optional
from sqlalchemy import delete, join, func

router= APIRouter(
    prefix='/posts',
    tags= ['[Posts'])

@router.put("/{id}")
def update_post(id:int, api_post: schemas.post , db: session= Depends(get_db),current_user : int = Depends(oath2.get_current_user) ):
    # cursor.execute("""update posts set title=%s,
    # content=%s, published=%s WHERE id=%s RETURNING * """,(post.title,post.content, post.published,str(id)))
    # updated_post=cursor.fetchone()
    # conn.commit()
    post_query= db.query(models.Post).filter(models.Post.id == id)
    upd_post=post_query.first()
    if not upd_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail = f"post with id {id} not found")
    
    if upd_post.creator_id != oath2.get_current_user.id:
        raise HTTPException (status_code=status.HTTP_403_FORBIDDEN, detail="not authorised to perform requested action")

    
    post_query.update(api_post.dict(), synchronize_session=False)
    db.commit()
    return{'data': post_query.first() }


@router.get("/",status_code=status.HTTP_200_OK ,response_model= List[schemas.Postoutvotes])
def get_posts( db: session= Depends(get_db), current_user : int = Depends(oath2.get_current_user), limit : int= 10, skip: int = 0, search: Optional[str]=""):
    # cursor.execute("select * from posts")
    # posts=cursor.fetchall()
    post_returned= db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results=db.query(models.Post,func.count(models.Votes.post_id).label("votes")).join(models.Votes,models.Votes.post_id==models.Post.id, isouter=True ).group_by(models.Post.id).all()
    return results

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.postout)
def find_posts(id: int,db: session= Depends(get_db),current_user : int = Depends(oath2.get_current_user)):
    post_returned = db.query(models.Post).filter(models.Post.id == id).first()
    if not post_returned:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail = f"post with id {id} not found")
    return post_returned
    # cursor.execute(""" select * from posts where id = %s""",(str(id)))
    # post_returned= cursor.fetchone()
    # conn.commit()
    # if not post_returned:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail = f"post with id {id} not found")
    # return {'post': post_returned} 


@router.post("/createpost", status_code= status.HTTP_201_CREATED)
def create_posts(post: schemas.post, db: session= Depends(get_db), current_user : int = Depends(oath2.get_current_user)):
    #new_post=models.Post(title= post.title, content=post.content, published=post.published)
    print(current_user.email)
    new_post= models.Post(creator_id=current_user.id,**post.dict())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # cursor.execute("""insert into posts (title,content,published) VALUES(%s,%s,%s) RETURNING * """,(postcreated.title,postcreated.content,postcreated.published))
    # new_post=cursor.fetchone()
    # conn.commit()
    # return {'new post': "new post returned"}
    return { 'new post': new_post}

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: session= Depends(get_db),current_user : int = Depends(oath2.get_current_user)):
    post_todel = db.query(models.Post).filter(models.Post.id == id)
    if post_todel.first() == None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail = f"post with id {id} not found")
    if post_todel.creator_id != current_user.id:
        raise HTTPException (status_code=status.HTTP_403_FORBIDDEN, detail="not authorised to perform requested action")
    post_todel.delete(synchronize_session= False)

    db.commit()
    # cursor.execute("""DELETE from posts where id = %s""", (str(id)))
    # deleted_post= cursor.fetchone()
    return Response(status_code=status.HTTP_204_NO_CONTENT )