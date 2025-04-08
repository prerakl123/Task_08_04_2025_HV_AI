from sqlalchemy.orm import Session

from exceptions import APIException
from models import Team, User, TeamMember


class TeamService:
    @staticmethod
    def create_team(db: Session, name: str, user_id: int):
        """Create a new team in the database."""
        new_team = Team(name=name, created_by=user_id)
        db.add(new_team)
        db.commit()
        db.refresh(new_team)
        return new_team

    @staticmethod
    def add_member(db: Session, team_id: int, user_id: int):
        """Add a user to a team."""
        team = db.query(Team).filter_by(id=team_id).first()
        if not team:
            raise APIException("Team not found", status_code=404)

        user = db.query(User).filter_by(id=user_id).first()
        if not user:
            raise APIException("User not found", status_code=404)

        if db.query(TeamMember).filter_by(team_id=team_id, user_id=user_id).first():
            raise APIException("User already a member of the team")

        member = TeamMember(team_id=team_id, user_id=user_id)
        db.add(member)
        db.commit()
        db.refresh(member)
        return member
