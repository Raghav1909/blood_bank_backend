from fastapi import APIRouter, Depends, Response, status, HTTPException
from app import models, utils, oauth2
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
    )


@router.post('/login')
def login(response: Response, user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data={"email": user.email})
    refresh_token = oauth2.create_refresh_token(data={"email": user.email})

    oauth2.set_jwt_cookie(response, access_token, refresh_token)


@router.post('/refresh')
def refresh(response: Response, db: Session = Depends(get_db)):
    oauth2.set_jwt_cookie(response)