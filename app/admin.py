from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db
from app.auth import get_current_admin_user

router = APIRouter(prefix="/admin", tags=["Admin"])

# ==================== USER MANAGEMENT ====================

@router.get("/users", response_model=schemas.UserListResponse)
def get_all_users(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        admin: models.User = Depends(get_current_admin_user)
):
    """Get all users (admin only)"""
    users = db.query(models.User).offset(skip).limit(limit).all()
    total = db.query(models.User).count()

    return {
        "total": total,
        "users": users
    }

@router.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user_by_id(
        user_id: int,
        db: Session = Depends(get_db),
        admin: models.User = Depends(get_current_admin_user)
):
    """Get specific user by ID (admin only)"""
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user

@router.put("/users/{user_id}/role", response_model=schemas.UserResponse)
def update_user_role(
        user_id: int,
        role_update: schemas.UserUpdateRole,
        db: Session = Depends(get_db),
        admin: models.User = Depends(get_current_admin_user)
):
    """Update user role (admin only)"""
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Don't allow admin to change their own role (prevents lockout)
    if user.id == admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change your own role"
        )

    user.role = role_update.role
    db.commit()
    db.refresh(user)

    return user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
        user_id: int,
        db: Session = Depends(get_db),
        admin: models.User = Depends(get_current_admin_user)
):
    """Delete a user (admin only)"""
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Don't allow admin to delete themselves
    if user.id == admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )

    db.delete(user)
    db.commit()
    return None

# ==================== TODO MANAGEMENT ====================

@router.get("/todos", response_model=schemas.TodoListResponse)
def get_all_todos(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        admin: models.User = Depends(get_current_admin_user)
):
    """Get all todos from all users (admin only)"""
    todos = db.query(models.Todo).offset(skip).limit(limit).all()
    total = db.query(models.Todo).count()

    return {
        "total": total,
        "todos": todos
    }

@router.get("/users/{user_id}/todos", response_model=List[schemas.TodoResponse])
def get_user_todos(
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        admin: models.User = Depends(get_current_admin_user)
):
    """Get all todos for a specific user (admin only)"""
    # Check if user exists
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    todos = db.query(models.Todo).filter(
        models.Todo.owner_id == user_id
    ).offset(skip).limit(limit).all()

    return todos