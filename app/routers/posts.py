from fastapi import Response, status, HTTPException, Depends, APIRouter
from database import get_db
from sqlalchemy.orm import Session
from schemas import PostCreate, Post, PostOut
from typing import List, Optional
import models
from sqlalchemy import func
from oauth2 import get_current_user

router = APIRouter(prefix="/posts", tags=["POSTS"])


@router.get("", response_model=List[PostOut])
def get_posts(
    db: Session = Depends(get_db), limit: int = 20, search: Optional[str] = ""
):

    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
    )

    posts = results.filter(models.Post.title.contains(search)).limit(limit).all()
    return posts


@router.get("/user_posts", response_model=List[PostOut])
def get_posts_by_user(
    db: Session = Depends(get_db), user: int = Depends(get_current_user)
):
    posts = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.user_id == user.id)
        .all()
    )
    return posts


@router.get("/{id}", response_model=PostOut)
def get_post(id: int, db: Session = Depends(get_db)):

    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return post


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    post = models.Post(user_id=user_id.id, **post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)
):

    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    if deleted_post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} doesn't exist",
        )
    post = deleted_post.first()
    if post.user_id != int(user_id.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorised to perform requested action.",
        )

    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=Post)
def update_post(
    id: int,
    post: PostCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    x = post.dict()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} doesn't exist",
        )
    if post.user_id != int(user_id.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorised to perform requested action.",
        )

    post_query.update(x, synchronize_session=False)
    db.commit()

    return post_query.first()
