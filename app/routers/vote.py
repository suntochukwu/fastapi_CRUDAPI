from fastapi import Body, Depends, FastAPI, Response,status, HTTPException, APIRouter
from app import schemas , database, oath2, models
from sqlalchemy.orm import session 

router= APIRouter(
    prefix='/vote',
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote , db: session=Depends(database.get_db),current_user: int = Depends(oath2.get_current_user)):
    
    post= db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post {vote.post_id} does not exist")


    vote_query=db.query(models.Votes).filter(models.Votes.post_id==vote.post_id, models.Votes.user_id == current_user.id)
    found_vote=vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f" user {current_user.id} has already liked")
        new_vote = models.Votes(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"succesfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return{"message":"succesfully deleted vote"}



    