# Team Feedback Management System

A Flask-based RESTful API for managing teams and peer feedback within an organization.

## Features

- User authentication with JWT tokens
- Role-based access control (Admin and Member roles)
- Team management
- Peer feedback submission and review
- Feedback summaries and detailed reports

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with the following variables:
```
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
SQLALCHEMY_DATABASE_URI=sqlite:///./app.db
```

4. Initialize the database:
```bash
python app.py
```

## API Endpoints

### Authentication

#### Register User
- **POST** `/register`
- Body:
```json
{
    "name": "string",
    "email": "user@example.com",
    "password": "string",
    "role": "admin|member"
}
```

#### Login
- **POST** `/login`
- Body:
```json
{
    "email": "user@example.com",
    "password": "string"
}
```

### Team Management

#### Create Team (Admin only)
- **POST** `/teams`
- Requires: JWT token
- Body:
```json
{
    "name": "string"
}
```

#### Add Team Member
- **POST** `/teams/{team_id}/add-member`
- Requires: JWT token
- Body:
```json
{
    "user_id": integer
}
```

### Feedback Management

#### Submit Feedback
- **POST** `/teams/{team_id}/feedback`
- Requires: JWT token
- Body:
```json
{
    "reviewee_id": integer,
    "rating": integer,
    "comment": "string"
}
```

#### View Feedback Summary
- **GET** `/teams/{team_id}/feedback-summary`
- Requires: JWT token
- Returns anonymous feedback summary for the team

#### View Detailed Feedback (Admin only)
- **GET** `/teams/{team_id}/detailed-feedback`
- Requires: Admin JWT token
- Returns detailed feedback including reviewer information

## Data Models

### User
- id: Integer (Primary Key)
- name: String
- email: String (Unique)
- password: String (Hashed)
- role: String ('admin' or 'member')

### Team
- id: Integer (Primary Key)
- name: String
- created_by: Integer (Foreign Key to User)

### TeamMember
- id: Integer (Primary Key)
- team_id: Integer (Foreign Key to Team)
- user_id: Integer (Foreign Key to User)

### Feedback
- id: Integer (Primary Key)
- team_id: Integer (Foreign Key to Team)
- reviewer_id: Integer (Foreign Key to User)
- reviewee_id: Integer (Foreign Key to User)
- rating: Integer
- comment: Text
- created_at: DateTime

## Error Handling

The API includes comprehensive error handling for:
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

## Security Features

- JWT-based authentication
- Role-based access control
- Password hashing
- Database session management
- Input validation using Pydantic
