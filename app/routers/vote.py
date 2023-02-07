from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix='/vote', tags=['Vote']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == vote.post_id)
    post = post_query.first()
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    print(found_vote)


    if post != None:
        if vote.dir == 1:
            if found_vote != None:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'User {current_user.id} has already voted on post {vote.post_id}')

            else:
                new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
                db.add(new_vote)
                post.votes += 1
                post_query.update({'votes': post.votes}, synchronize_session=False)
                db.commit()
                return {"message": "succesfully added vote"}

        else:
            if found_vote == None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User {current_user.id} did not vote on post {vote.post_id} previously')

            else:
                vote_query.delete(synchronize_session=False)
                post.votes -= 1
                post_query.update({'votes': post.votes}, synchronize_session=False)
                db.commit()
                return {"message": "succesfully deleted vote"}

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {vote.post_id} does not exist')