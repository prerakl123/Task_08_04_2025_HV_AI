from exceptions import APIException
from models import Feedback, TeamMember, User
from sqlalchemy.orm import Session
from sqlalchemy import func


class FeedbackService:
    """Service class for handling feedback-related operations."""

    @staticmethod
    def submit_feedback(db: Session, team_id: int, reviewer_id: int, reviewee_id: int, rating: int, comment: str):
        """Check both reviewer and reviewee are part of the team"""
        for uid in [reviewer_id, reviewee_id]:
            if not db.query(TeamMember).filter_by(team_id=team_id, user_id=uid).first():
                raise APIException(f"User '{uid}' is not part of the team")

        fb = Feedback(
            team_id=team_id,
            reviewer_id=reviewer_id,
            reviewee_id=reviewee_id,
            rating=rating,
            comment=comment,
        )
        db.add(fb)
        db.commit()
        db.refresh(fb)
        return fb

    @staticmethod
    def get_summary(db: Session, team_id: int):
        """Get the anonymous summary of feedback for a team."""
        results = (
            db.query(
                Feedback.reviewee_id,
                func.avg(Feedback.rating).label("avg_rating"),
                func.count(Feedback.id).label("feedback_count"),
                func.array_agg(Feedback.comment).label("comments")
            )
            .filter(Feedback.team_id == team_id)
            .group_by(Feedback.reviewee_id)
            .all()
        )

        return [
            {
                "reviewee_id": r.reviewee_id,
                "avg_rating": round(r.avg_rating, 2),
                "feedback_count": r.feedback_count,
                "comments": r.comments  # Comments are included but without reviewer information
            }
            for r in results
        ]

    @staticmethod
    def get_detailed_feedback(db: Session, team_id: int, is_admin: bool):
        """Get detailed feedback including reviewer information for admin purposes."""
        if not is_admin:
            raise APIException("Unauthorized access", status_code=403)

        feedbacks = (
            db.query(Feedback)
            .filter(Feedback.team_id == team_id)
            .all()
        )

        return [
            {
                "id": f.id,
                "reviewer_id": f.reviewer_id,
                "reviewee_id": f.reviewee_id,
                "rating": f.rating,
                "comment": f.comment,
                "created_at": f.created_at
            }
            for f in feedbacks
        ]
