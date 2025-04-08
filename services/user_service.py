from sqlalchemy.orm import Session

from exceptions import APIException
from models import User
from werkzeug.security import generate_password_hash, check_password_hash


class UserService:
    @staticmethod
    def register_user(db: Session, name: str, email: str, password: str, role: str):
        """Registers a new user in the database."""
        if db.query(User).filter_by(email=email).first():
            raise APIException("User already exists")

        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password, role=role)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str):
        """Authenticates a user by checking the email and password."""
        user = db.query(User).filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return None
        return user
