from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix='/posts', tags=['Posts']
)

# @router.get('/sqlalchemy')
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {'data': 'success'}

@router.get('/', response_model=List[schemas.ResponseBase])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ''):
    # USING RAW SQL
    # cursor.execute('''SELECT * FROM posts''')
    # posts = cursor.fetchall()

    # USING AN ORM (SQLALCHEMY)
    posts = db.query(models.Post).filter(models.Post.title.contains(search) == True).limit(limit).offset(skip).all()
    # results = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    
    # for post in posts:
    #     for result in results:
    #         if result.Post.id == post.id:
    #             post.votes = result[1]
    
    db.commit()
    return posts

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseBase)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # USING RAW SQL
    # cursor.execute('''INSERT INTO posts (title, content, published, rating) VALUES (%s, %s, %s, %s) RETURNING * ''', (post.title, post.content, post.published, post.rating))
    # new_post = cursor.fetchone()
    # conn.commit()
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)

    # USING AN ORM (SQLALCHEMY)
    new_post = models.Post(user_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get('/{id}', response_model=schemas.ResponseBase)
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # USING RAW SQL
    # cursor.execute('''SELECT * FROM posts WHERE id = %s ''', (str(id)))
    # post = cursor.fetchone()

    # USING AN ORM (SQLALCHEMY)
    post =  db.query(models.Post).filter(models.Post.id == id).first()

    if post != None:
        return post

    elif post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {id} was not found')

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # USING RAW SQL
    # cursor.execute('''DELETE FROM posts WHERE id = %s RETURNING * ''', (str(id),))
    # post = cursor.fetchone()
    # conn.commit()

    # USING AN ORM (SQLALCHEMY)
    post =  db.query(models.Post).filter(models.Post.id == id)
    if post.first() != None:
        if post.first().user_id == current_user.id:
            post.delete(synchronize_session=False)
            db.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Not authorized to perform requested action')

    elif post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {id} does not exist')

@router.put('/{id}', response_model=schemas.ResponseBase)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # USING RAW SQL
    # cursor.execute('''UPDATE posts SET title = %s, content = %s, published = %s, rating = %s WHERE id = %s RETURNING * ''', (post.title, post.content, post.published, post.rating, str(id)))
    # post = cursor.fetchone()
    # conn.commit()

    # USING AN ORM (SQLALCHEMY)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post != None:
        if post.user_id == current_user.id:
            post_query.update(updated_post.dict(), synchronize_session=False)
            db.commit()
            return post_query.first()

        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Not authorized to perform requested action')
            
    elif post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {id} does not exist')