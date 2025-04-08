from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserRegister(UserBase):
    """Schema for user registration"""
    password: str
    role: str


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class UserOut(UserBase):
    """Schema for user output"""
    id: int
    role: str

    class Config:
        from_attributes = True


class TeamCreate(BaseModel):
    """Schema for creating a new team"""
    name: str


class TeamOut(BaseModel):
    """Schema for team output"""
    id: int
    name: str
    created_by: int

    class Config:
        from_attributes = True


class AddMember(BaseModel):
    """Schema for adding a member to a team"""
    user_id: int


class FeedbackCreate(BaseModel):
    """Schema for submitting feedback"""
    reviewee_id: int
    rating: int
    comment: str


class FeedbackSummary(BaseModel):
    """Schema for summarizing feedback"""
    reviewee_id: int
    avg_rating: float
    feedback_count: int
