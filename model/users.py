from sqlalchemy import Column, Integer, String, DateTime, func
from db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    contact = Column(String(15), nullable=True)           # Changed to String for phone numbers
    dob = Column(DateTime, nullable=True)                 # Date of birth, no default timestamp
    password = Column(String(255), nullable=False)         # Use String for hashed passwords
    created_at = Column(DateTime, default=func.now())      # Added creation timestamp
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Auto update timestamp
