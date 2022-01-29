from fastapi import FastAPI, status, HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
import sqlalchemy

from .. import schemas, utils
from ..db import models
from ..db.database import get_db

router = APIRouter(
    tags=["Users"],
    prefix="/user"
)


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User {user.email} is already registered")

    return new_user
