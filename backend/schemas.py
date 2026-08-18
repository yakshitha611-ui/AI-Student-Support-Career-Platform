from datetime import date, datetime

from pydantic import BaseModel, EmailStr, field_validator


class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class StudentProfileBase(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    university: str | None = None
    branch: str | None = None
    year_of_study: str | None = None
    current_semester: str | None = None
    cgpa_percentage: str | None = None

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str | None):
        if value is None or value == "":
            return value
        digits = "".join(ch for ch in value if ch.isdigit())
        if len(digits) < 10 or len(digits) > 15:
            raise ValueError("Phone number must contain 10 to 15 digits.")
        return value.strip()

    @field_validator("cgpa_percentage")
    @classmethod
    def validate_cgpa_percentage(cls, value: str | None):
        if value is None or value == "":
            return value
        try:
            numeric_value = float(str(value).strip())
        except ValueError:
            raise ValueError("CGPA/percentage must be a valid number.")
        if numeric_value < 0 or numeric_value > 100:
            raise ValueError("CGPA/percentage should be between 0 and 100.")
        return str(numeric_value)


class StudentProfileCreate(StudentProfileBase):
    full_name: str
    email: EmailStr


class StudentProfileUpdate(StudentProfileBase):
    pass


class StudentProfileResponse(StudentProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ChatMessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class ChatResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime
    messages: list[ChatMessageResponse]

    class Config:
        from_attributes = True


class ChatListResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ChatMessageRequest(BaseModel):
    content: str


class ChatbotResponse(BaseModel):
    response: str
    context_used: dict | None = None
