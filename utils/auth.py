from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity

from models import User
from database import SessionLocal


def is_admin(user_id: int) -> bool:
    """Check if the user is an admin."""
    db = SessionLocal()
    user = db.query(User).filter_by(id=user_id).first()
    db.close()
    return user and user.role == "admin"


def role_required(role):
    """Decorator to check if the user has the required role."""

    def decorator(func):
        """Decorator to check if the user has the required role."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            db = SessionLocal()
            user = db.query(User).filter_by(id=user_id).first()
            db.close()
            if not user or user.role != role:
                return jsonify({"error": "Unauthorized"}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator
