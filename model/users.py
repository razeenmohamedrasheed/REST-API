from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
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
    
    tasks = relationship("Tasks", back_populates="user", cascade="all, delete-orphan")

class Tasks(Base):
    __tablename__ = "tasks"
    task_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    username = Column(String(50), nullable=False)
    taskname = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=func.now())      # Added creation timestamp
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Auto update timestamp

    user = relationship("User", back_populates="tasks")