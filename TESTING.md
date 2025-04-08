# API Testing Sequence with Postman

## 1. Register Users
### Register Admin User
POST http://localhost:5000/register
```json
{
    "name": "Admin User",
    "email": "admin@example.com",
    "password": "admin123",
    "role": "admin"
}
```

### Register Regular Users
POST http://localhost:5000/register
```json
{
    "name": "User One",
    "email": "user1@example.com",
    "password": "user123",
    "role": "user"
}
```

POST http://localhost:5000/register
```json
{
    "name": "User Two",
    "email": "user2@example.com",
    "password": "user123",
    "role": "user"
}
```

## 2. Login
### Login as Admin
POST http://localhost:5000/login
```json
{
    "email": "admin@example.com",
    "password": "admin123"
}
```
*Save the returned access_token for subsequent admin requests*

### Login as User One
POST http://localhost:5000/login
```json
{
    "email": "user1@example.com",
    "password": "user123"
}
```
*Save the returned access_token for subsequent user requests*

## 3. Create Team (Admin only)
POST http://localhost:5000/teams
Headers:
- Authorization: Bearer {admin_access_token}
```json
{
    "name": "Test Team"
}
```
*Note the team_id from response*

## 4. Add Team Members
POST http://localhost:5000/teams/{team_id}/add-member
Headers:
- Authorization: Bearer {admin_access_token}
```json
{
    "user_id": 2
}
```

POST http://localhost:5000/teams/{team_id}/add-member
Headers:
- Authorization: Bearer {admin_access_token}
```json
{
    "user_id": 3
}
```

## 5. Submit Feedback
### Submit feedback as User One
POST http://localhost:5000/teams/{team_id}/feedback
Headers:
- Authorization: Bearer {user1_access_token}
```json
{
    "reviewee_id": 3,
    "rating": 4,
    "comment": "Great team player!"
}
```

### Submit feedback as User Two
POST http://localhost:5000/teams/{team_id}/feedback
Headers:
- Authorization: Bearer {user2_access_token}
```json
{
    "reviewee_id": 2,
    "rating": 5,
    "comment": "Excellent communication skills"
}
```

## 6. View Feedback
### View Anonymous Feedback Summary
GET http://localhost:5000/teams/{team_id}/feedback-summary
Headers:
- Authorization: Bearer {user1_access_token}

### View Detailed Feedback (Admin only)
GET http://localhost:5000/teams/{team_id}/detailed-feedback
Headers:
- Authorization: Bearer {admin_access_token}

## Error Testing Scenarios
1. Try to create team with non-admin user
2. Try to add non-existent user to team
3. Try to submit feedback for user not in team
4. Try to access detailed feedback with non-admin user
5. Try to register with duplicate email
