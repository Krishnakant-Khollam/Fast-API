from fastapi import Response, status, HTTPException, Depends, APIRouter
from database import get_db
from sqlalchemy.orm import Session
from schemas import UserCreate, User
from typing import List
import models
from utils import hash

router = APIRouter(prefix="/users", tags=["USERS"])


@router.get("", response_model=List[User])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get("/{id}", response_model=User)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id: {id} was not found",
        )
    return user


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_post = db.query(models.User).filter(models.User.email == user.email)
    if user_post:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User with email {user.email} already exists.",
        )

    hashed_passwd = hash(user.password)
    user.password = hashed_passwd
    user = models.User(**user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):

    deleted_user = db.query(models.User).filter(models.User.id == id)
    if deleted_user.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id {id} doesn't exist",
        )
    deleted_user.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
