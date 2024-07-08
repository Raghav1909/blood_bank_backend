from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship

from .database import Base

blood_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
blood_components = ["Whole", "Plasma", "Platelets", "RBC"]
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
    blood_repository = relationship("BloodRepository", foreign_keys='BloodRepository.donated_by', back_populates="donor")
    received_blood = relationship("BloodRepository", foreign_keys='BloodRepository.received_by', back_populates="receiver")
    requests = relationship("Request", back_populates="donor")


class Donation(Base):
    __tablename__ = "donations"
    
    id = Column(Integer, primary_key=True, index=True)
    donor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    donated_on = Column(Date, nullable=False)
    is_whole = Column(Boolean, nullable=False)
    blood_component_id = Column(Integer, ForeignKey("blood_components.id"), nullable=False)
    
    donor = relationship("User", back_populates="donations")
    blood_component = relationship("BloodComponent")


class BloodComponent(Base):
    __tablename__ = "blood_components"
    
    id = Column(Integer, primary_key=True, index=True)
    blood_group = Column(Enum(*blood_groups, name="blood_groups"), nullable=False)
    name = Column(Enum(*blood_components[1:], name="blood_components"), nullable=False)
    expiry_in_days = Column(Integer, nullable=False)
    
    donations = relationship("Donation")
    requests = relationship("Request")


class BloodRepository(Base):
    __tablename__ = "repository"
    
    id = Column(Integer, primary_key=True, index=True)
    is_expired = Column(Boolean, nullable=False)
    donated_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    received_by = Column(Integer, ForeignKey("users.id"))
    
    donor = relationship("User", foreign_keys=[donated_by], back_populates="blood_repository")
    receiver = relationship("User", foreign_keys=[received_by], back_populates="received_blood")


class Request(Base):
    __tablename__ = "requests"
    
    id = Column(Integer, primary_key=True, index=True)
    donor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    blood_group = Column(Enum(*blood_groups, name="blood_groups"), nullable=False)
    blood_component_id = Column(Integer, ForeignKey("blood_components.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(Enum(*status, name="status"), nullable=False)
    
    donor = relationship("User", back_populates="requests")
    blood_component = relationship("BloodComponent", back_populates="requests")


class FulfilledRequest(Base):
    __tablename__ = "fulfilled_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("requests.id"), nullable=False)
    date = Column(Date, nullable=False)
    donor_ids = Column(String, nullable=False)
    
    request = relationship("Request")
