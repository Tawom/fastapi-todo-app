from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional, List
from datetime import datetime

# Role constants
class UserRole:
    ADMIN = "admin"
    USER = "user"

# ==================== User Schemas ====================

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    password: str = Field(..., min_length=8, max_length=72)
    role: str = UserRole.USER
    phone_number: Optional[str] = None

    @field_validator('password')
    def validate_password(cls, v):
        if len(v.encode('utf-8')) > 72:
            raise ValueError('Password too long for bcrypt (max 72 bytes)')
        return v

    @field_validator('role')
    def validate_role(cls, v):
        if v not in [UserRole.ADMIN, UserRole.USER]:
            raise ValueError(f'Role must be either "{UserRole.ADMIN}" or "{UserRole.USER}"')
        return v

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    first_name: str
    last_name: str
    is_active: bool
    role: str
    phone_number: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
# ==================== Password Management Schemas ====================

class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=72)

    @field_validator('new_password')
    def validate_new_password(cls, v):
        if len(v.encode('utf-8')) > 72:
            raise ValueError('Password too long for bcrypt (max 72 bytes)')
        return v

class PasswordChangeResponse(BaseModel):
    message: str
    timestamp: datetime

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8, max_length=72)

    @field_validator('new_password')
    def validate_new_password(cls, v):
        if len(v.encode('utf-8')) > 72:
            raise ValueError('Password too long for bcrypt (max 72 bytes)')
        return v

# ==================== Admin Schemas ====================

class UserUpdateRole(BaseModel):
    role: str

    @field_validator('role')
    def validate_role(cls, v):
        if v not in [UserRole.ADMIN, UserRole.USER]:
            raise ValueError(f'Role must be either "{UserRole.ADMIN}" or "{UserRole.USER}"')
        return v

class UserListResponse(BaseModel):
    total: int
    users: List[UserResponse]

# ==================== Todo Schemas ====================

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TodoResponse(TodoBase):
    id: int
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True

class TodoListResponse(BaseModel):
    total: int
    todos: List[TodoResponse]