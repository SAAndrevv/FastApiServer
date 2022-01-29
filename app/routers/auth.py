from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from ..db.database import get_db
from ..db import models
from .. import schemas, utils, oauth2

router = APIRouter(tags=["Authentication"])

#OAuth2PasswordRequestForm = Depends()
#schemas.UserLogin
@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")

    access_token = oauth2.create_access_token(data={"id_user": user.id_user,
                                                    "role": "owner"})
    return {"access_token": access_token, "token_type": "bearer"}
