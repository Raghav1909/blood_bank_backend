from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from routers import auth, hospitals, staff, requests, donors, donations, repository
from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware( 
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(auth.router)
# app.include_router(hospitals.router)
# app.include_router(staff.router)
# app.include_router(requests.router)
# app.include_router(donors.router)
# app.include_router(donations.router)
# app.include_router(repository.router)

@app.get("/")
async def root():
    return "Blood Bank System"