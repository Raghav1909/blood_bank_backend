from fastapi import Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime, timedelta, UTC
from app import schemas, models
from app.config import settings
from app.database import get_db
from sqlalchemy.orm import Session

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_MINUTES = settings.refresh_token_expire_minutes


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_access_token(data: dict):
    """
    Creates an access token by encoding the input data in a JWT token.
    
    Parameters:
        - data (dict): The data to be encoded in the token (email, role, access in this case).
    
    Returns:
        - str: The encoded JWT access token.
    """
    to_encode = data.copy()

    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def create_refresh_token(data: dict):
    """
    Creates a refresh token by encoding the input data in a JWT token.
    
    Parameters:
        - data (dict): The data to be encoded in the token (email).
    
    Returns:
        - str: The encoded JWT refresh token.
    """
    to_encode = data.copy()
    
    expire = datetime.now(UTC) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    """
    Verify the access token by decoding the token using the secret key and algorithm.
    
    Parameters:
    - token (str): The access token to be verified.
    - credentials_exception: The exception to be raised if credentials are invalid.
    
    Returns:
    - TokenData: The token data containing the user's email.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        email: str = payload.get("email")
        
        if email == "":
            raise credentials_exception
        
        token_data = schemas.TokenData(email=email)
    
    except Exception:
        raise credentials_exception
    
    return token_data


def set_jwt_cookie(response: Response, access_token: str, refresh_token: str | None = None):
    """
    Sets a JWT cookie in the response.

    Parameters:
        - response (Response): The response object to set the cookie.
        - access_token (str): The JWT access token to be set as the cookie value.
        - refresh_token (str, optional): The JWT refresh token to be set as the cookie value.
            Defaults to None.

    Returns:
        None
    """
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,  
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        secure=False,  
        samesite="lax",
    )
    
    if refresh_token:
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60, 
            secure=False,  
            samesite="lax",
        )


def unset_jwt_cookie(response: Response):
    """
    Delete the JWT cookie from the response.

    Args:
        response (Response): The response object to delete the cookie from.

    Returns:
        None

    This function deletes the JWT cookie with the key "access_token" from the given response object.
    The cookie is set to be HTTP-only and has no expiration time.
    """
    response.delete_cookie(
        key="access_token",
        httponly=True,
    )
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
    )


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Get the current user based on the provided access token.

    Args:
        token (str, optional): The access token to verify. Defaults to Depends(oauth2_scheme).
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        User
    """
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    token_data = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.email == token_data.email).first()
    return user