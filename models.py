from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship, declarative_base

# Base class for all SQLAlchemy models
Base = declarative_base()


class User(Base):
    """Model representing a user in the system"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(10), nullable=False)  # 'admin' or 'member'

    # Relationships
    teams = relationship("Team", back_populates="creator", cascade="all, delete")
    feedback_given = relationship("Feedback", foreign_keys='Feedback.reviewer_id', back_populates="reviewer")
    feedback_received = relationship("Feedback", foreign_keys='Feedback.reviewee_id', back_populates="reviewee")


class Team(Base):
    """Model representing a team"""
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"))

    # Relationships
    creator = relationship("User", back_populates="teams")
    members = relationship("TeamMember", back_populates="team", cascade="all, delete-orphan")
    feedback = relationship("Feedback", back_populates="team", cascade="all, delete")


class TeamMember(Base):
    """Model representing a member of a team"""
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationships
    team = relationship("Team", back_populates="members")
    user = relationship("User")


class Feedback(Base):
    """Model representing feedback given by a user to another user within a team"""
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reviewee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    team = relationship("Team", back_populates="feedback")
    reviewer = relationship("User", foreign_keys=[reviewer_id], back_populates="feedback_given")
    reviewee = relationship("User", foreign_keys=[reviewee_id], back_populates="feedback_received")
