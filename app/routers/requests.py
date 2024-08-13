from fastapi import APIRouter, Depends, status, HTTPException
from app import models, schemas
from app.database import get_db
from sqlalchemy.orm import Session
from app.oauth2 import get_current_user


router = APIRouter(
    prefix='/requests',
    tags=['Requests']
)