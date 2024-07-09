from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .database import Base

blood_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
blood_components = ["Plasma", "Platelets", "RBC"]
status = ["PENDING", "SUCCESS", "FAILED"]

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True)
    phone_no = Column(String, unique=True, nullable=True)
    password = Column(String, nullable=False)
    dob = Column(Date, nullable=True)
    
    donations = relationship("Donation", back_populates="donor")
    requests = relationship("Request", back_populates="user")

class Donation(Base):
    __tablename__ = "donations"
    
    id = Column(Integer, primary_key=True, index=True)
    donor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    donated_on = Column(Date, nullable=False)
    is_whole = Column(Boolean, nullable=False)
    blood_component_id = Column(Integer, ForeignKey("blood_components.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    
    donor = relationship("User", back_populates="donations")

class BloodComponent(Base):
    __tablename__ = "blood_components"
    
    id = Column(Integer, primary_key=True, index=True)
    blood_group = Column(Enum(*blood_groups, name="blood_groups"), nullable=False)
    component_name = Column(Enum(*blood_components, name="blood_components"), nullable=False)
    expiry_in_days = Column(Integer, nullable=False)

class BloodRepository(Base):
    __tablename__ = "repository"
    
    id = Column(Integer, primary_key=True, index=True)
    expiry_date = Column(Date, nullable=False)
    donated_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    blood_component_id = Column(Integer, ForeignKey("blood_components.id"), nullable=False)
    
    donors = relationship("User", backref="repository")
    blood_components = relationship("BloodComponent", backref="repository")

class Request(Base):
    __tablename__ = "requests"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    blood_group = Column(Enum(*blood_groups, name="blood_groups"), nullable=False)
    blood_component_id = Column(Integer, ForeignKey("blood_components.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(Enum(*status, name="status"), nullable=False)
    
    user = relationship("User", back_populates="requests")
    blood_components = relationship("BloodComponent", backref="requests")

class FulfilledRequest(Base):
    __tablename__ = "fulfilled_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("requests.id"), nullable=False)
    date = Column(Date, nullable=False)
    donor_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    requests = relationship("Request", backref="fulfilled_requests")
    donors = relationship("User", backref="fulfilled_requests")