from typing import List

from fastapi import status, HTTPException, APIRouter, Body
from fastapi.params import Depends
from sqlalchemy.orm import Session

from .. import schemas, oauth2
from ..db import models
from ..db.database import get_db

router = APIRouter(
    tags=["Qr"],
    prefix="/qr"
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Token)
def create_qr_token(post: schemas.UserAccessData, db: Session = Depends(get_db),
                    current_user: schemas.UserToken = Depends(oauth2.get_current_user_data)):
    if current_user.role not in ["owner"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Access denied")

    access_token = oauth2.create_shared_token(data={"id_user": current_user.id_user,
                                                    "role": "shared",
                                                    "data": post.data})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/", response_model=schemas.UserAccessData)
def get_qr_data(current_user: schemas.UserToken = Depends(oauth2.get_current_user_data)):
    return {"data": current_user.data}
