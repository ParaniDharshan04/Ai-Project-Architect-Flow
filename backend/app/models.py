from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    projects = relationship("Project", back_populates="user")

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    project_name = Column(String, nullable=False)
    description = Column(Text)
    tech_stack = Column(Text)
    features = Column(Text)
    installation_steps = Column(Text)
    extra_notes = Column(Text)
    generated_readme = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="projects")
