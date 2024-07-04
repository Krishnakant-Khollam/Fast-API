from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from database import get_db
from sqlalchemy.orm import Session
import models
from utils import verify
from schemas import Token
from oauth2 import create_access_token

router = APIRouter(prefix="/login", tags=["AUTHENTICATION"])


@router.post("/", response_model=Token)
def login(
    user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == user_cred.username).first()
    if user == None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"INVALID CREDENTIALS",
        )
    if not verify(user_cred.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"INVALID CREDENTIALS",
        )

    access_token = create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
