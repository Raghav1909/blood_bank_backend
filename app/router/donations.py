from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from app.database import get_db
from app import models, schemas
from sqlalchemy.orm import Session


router = APIRouter(
    prefix='/donations',
    tags=['Donations']
)


@router.get("/")
def get_donations(db: Session = Depends(get_db)):
    donations = db.query(models.Donation).all()
    return donations


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_donation(donation: schemas.DonationCreate, db: Session = Depends(get_db)):
    db_donation = models.Donation(**donation.model_dump())
    db.add(db_donation)
    db.commit()
    db.refresh(db_donation)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"id": db_donation.id})