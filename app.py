from flask import Flask, request, jsonify, g
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required

from config import Config
from database import init_db, SessionLocal, engine
from exceptions import APIException
from models import Base
from schemas import AddMember, FeedbackCreate
from schemas import UserRegister, UserLogin, TeamCreate, UserOut, TeamOut
from services.feedback_service import FeedbackService
from services.team_service import TeamService
from services.user_service import UserService
from utils.auth import is_admin, role_required

# Initialize Flask application
app = Flask(__name__)

# Load configuration from config.py
app.config.from_object(Config)

# Initialize JWT manager for handling authentication
jwt = JWTManager(app)

# Initialize database tables
Base.metadata.create_all(bind=engine)
init_db()


@app.before_request
def open_db_session():
    """Open a new database session before handling each request"""
    g.db = SessionLocal()


@app.teardown_request
def close_db_session(exception=None):
    """Close the database session after handling each request"""
    if exception:
        print(exception)

    db = g.pop('db', None)
    if db is not None:
        db.close()


# === Public Routes ===

@app.route("/register", methods=["POST"])
def register():
    """Endpoint to register a new user"""
    data = UserRegister(**request.json)
    db = g.db

    try:
        # Register the user using the UserService
        user = UserService.register_user(db, data.name, data.email, data.password, data.role)
        return jsonify(UserOut.model_validate(user).model_dump()), 201
    except ValueError as e:
        # Handle validation errors
        return jsonify({"error": str(e)}), 400


@app.route("/login", methods=["POST"])
def login():
    """Endpoint to authenticate a user and generate a JWT token"""
    data = UserLogin(**request.json)
    db = g.db

    # Authenticate the user
    user = UserService.authenticate_user(db, data.email, data.password)
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    # Generate an access token
    token = create_access_token(identity=user.id)
    return jsonify(access_token=token), 200


# === Protected Routes ===

@app.post("/teams")
@jwt_required()
@role_required("admin")
def create_team():
    """Endpoint to create a new team (admin-only)"""
    data = TeamCreate(**request.json)
    db = g.db

    # Get the ID of the currently authenticated user
    user_id = get_jwt_identity()
    if not is_admin(user_id):
        return jsonify({"error": "Only admins can create teams"}), 403

    # Create the team using the TeamService
    team = TeamService.create_team(db, data.name, user_id)
    return jsonify(TeamOut.model_validate(team).model_dump()), 201


@app.post("/teams/<int:team_id>/add-member")
@jwt_required()
def add_member(team_id):
    """Endpoint to add a member to a team"""
    data = AddMember(**request.json)
    db = g.db

    try:
        # Add the member to the team using the TeamService
        TeamService.add_member(db, team_id, data.user_id)
        return jsonify({"message": f"User {data.user_id} added to team {team_id}"}), 200
    except ValueError as e:
        # Handle validation errors
        return jsonify({"error": str(e)}), 400


@app.post("/teams/<int:team_id>/feedback")
@jwt_required()
def submit_feedback(team_id):
    """Endpoint to submit feedback for a team member"""
    data = FeedbackCreate(**request.json)
    db = g.db

    # Get the ID of the currently authenticated user
    reviewer_id = get_jwt_identity()
    try:
        # Submit the feedback using the FeedbackService
        FeedbackService.submit_feedback(
            db,
            team_id=team_id,
            reviewer_id=reviewer_id,
            reviewee_id=data.reviewee_id,
            rating=data.rating,
            comment=data.comment,
        )
        return jsonify({"message": "Feedback submitted"}), 201
    except ValueError as e:
        # Handle validation errors
        return jsonify({"error": str(e)}), 400


@app.get("/teams/<int:team_id>/feedback-summary")
@jwt_required()
def feedback_summary(team_id):
    """Endpoint to get a summary of feedback for a team"""
    db = g.db
    summary = FeedbackService.get_summary(db, team_id)
    return jsonify(summary), 200


@app.get("/teams/<int:team_id>/detailed-feedback")
@jwt_required()
@role_required("admin")
def detailed_feedback(team_id):
    """Admin endpoint to get detailed feedback including reviewer information"""
    db = g.db
    user_id = get_jwt_identity()
    summary = FeedbackService.get_detailed_feedback(db, team_id, is_admin(user_id))
    return jsonify(summary), 200


# === Error Handling ===

@app.errorhandler(APIException)
def handle_api_exception(e):
    """Handle custom API exceptions"""
    return jsonify({"error": e.message}), e.status_code


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({"error": f"Not found: '{e}'"}), 404


@app.errorhandler(500)
def internal_server_error(e):
    """Handle 500 errors"""
    return jsonify({"error": f"Internal server error: '{e}'"}), 500


if __name__ == "__main__":
    # Run the Flask application in debug mode
    app.run(debug=True)
