from fastapi import status, HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from .. import schemas, oauth2
from ..db import models
from ..db.database import get_db
from ..document import create_document, get_document
from ..schemas import IdDoc

router = APIRouter(
    tags=["Passport"],
    prefix="/passport"
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_passport(post: schemas.Passport, db: Session = Depends(get_db),
                 current_user: schemas.UserToken = Depends(oauth2.get_current_user_data)):
    if current_user.role not in ["owner"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Access denied")

    document = db.query(models.Documents).filter(models.Documents.id_user == current_user.id_user,
                                                 models.Documents.id_type == 1).first()

    if document:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Passport of user id {current_user.id_user} is already created")

    post = post.dict()
    post.pop("verifying")

    id_doc = create_document(db, current_user.id_user, 1, 1)
    new_passport = models.Passport(id_doc=id_doc.id_doc, **post)
    db.add(new_passport)
    db.commit()
    db.refresh(new_passport)

    return new_passport


@router.get("/", response_model=schemas.Passport)
def get_passport(db: Session = Depends(get_db),
                 current_user: schemas.UserToken = Depends(oauth2.get_current_user_data)):
    if current_user.role == "shared" and "PASSPORT" not in current_user.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Access denied")

    passport = get_document(db, models.Passport, current_user.id_user, 1)

    if not passport:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Passport of user id {current_user.id_user} was not found")

    new_passport = schemas.Passport.from_orm(passport[0])
    new_passport.verifying = passport[1]

    return new_passport


@router.put("/", response_model=schemas.Passport)
def update_passport(post: schemas.Passport, db: Session = Depends(get_db),
                    current_user: schemas.UserToken = Depends(oauth2.get_current_user_data)):
    if current_user.role not in ["owner"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Access denied")

    document = db.query(models.Documents).filter(models.Documents.id_user == current_user.id_user,
                                                 models.Documents.id_type == 1).first()

    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Passport of user id {current_user.id_user} does not exist")

    id_doc = IdDoc.from_orm(document)
    post = post.dict()
    post.pop("verifying")

    passport = db.query(models.Passport).filter(models.Passport.id_doc == id_doc.id_doc)

    passport.update(post, synchronize_session=False)
    db.commit()

    return passport.first()
