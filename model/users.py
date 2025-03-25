from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from db import Base


# Roles Table
class Roles(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, index=True)
    user_role = Column(String(50), unique=True, nullable=False)

    # Relationship with User table
    users = relationship("User", back_populates="role")

# User Table
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    user_role = Column(Integer, ForeignKey("roles.role_id", ondelete="CASCADE"), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    contact = Column(String(15), nullable=True)           # Phone number as String
    dob = Column(DateTime, nullable=True)                 # Date of birth
    password = Column(String(255), nullable=False)         # Hashed passwords
    created_at = Column(DateTime, default=func.now())      # Creation timestamp
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Auto update timestamp

    # Relationships
    tasks = relationship("Tasks", back_populates="user", cascade="all, delete-orphan")
    role = relationship("Roles", back_populates="users")

# Tasks Table
class Tasks(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    taskname = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="tasks")
