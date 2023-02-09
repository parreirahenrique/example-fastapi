from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, utils, oauth2, schemas
from ..database import get_db

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if user != None:
        
        if utils.verify(user_credentials.password, user.password) == True:
            access_token = oauth2.create_access_token(data={'user_id': user.id})
            
            return {'access_token': access_token, 'token_type': 'bearer'}

        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid credentials')
        
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid credentials')