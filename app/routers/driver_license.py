from fastapi import status, HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from .. import schemas, oauth2
from ..db import models
from ..db.database import get_db
from ..document import create_document, get_document
from ..schemas import IdDoc

router = APIRouter(
    tags=["Driver license"],
    prefix="/driver_license"
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.DriverLicense)
def add_driver_license(post: schemas.DriverLicense, db: Session = Depends(get_db),
                       current_user: schemas.UserToken = Depends(oauth2.get_current_user_data)):
    if current_user.role not in ["owner"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Access denied")

    document = db.query(models.Documents).filter(models.Documents.id_user == current_user.id_user,
                                                 models.Documents.id_type == 2).first()

    if document:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Driver license of user id {current_user.id_user} is already created")

    post = post.dict()
    post.pop("verifying")

    id_doc = create_document(db, current_user.id_user, 2, 1)
    new_license = models.DriverLicense(id_doc=id_doc.id_doc, **post)
    db.add(new_license)
    db.commit()
    db.refresh(new_license)

    return new_license


@router.get("/", response_model=schemas.DriverLicense)
def get_driver_license(db: Session = Depends(get_db),
                       current_user: schemas.UserToken = Depends(oauth2.get_current_user_data)):
    if current_user.role == "shared" and "DRIVER_LICENSE" not in current_user.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Access denied")

    get_license = get_document(db, models.DriverLicense, current_user.id_user, 2)

    if not get_license:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Driver license of user id {current_user.id_user} was not found")

    new_license = schemas.DriverLicense.from_orm(get_license[0])
    new_license.verifying = get_license[1]

    return new_license


@router.put("/", response_model=schemas.DriverLicense)
def update_driver_license(post: schemas.DriverLicense, db: Session = Depends(get_db),
                          current_user: schemas.UserToken = Depends(oauth2.get_current_user_data)):
    if current_user.role not in ["owner"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Access denied")

    document = db.query(models.Documents).filter(models.Documents.id_user == current_user.id_user,
                                                 models.Documents.id_type == 2).first()

    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Driver license of user id {current_user.id_user} does not exist")

    id_doc = IdDoc.from_orm(document)
    post = post.dict()
    post.pop("verifying")

    license_query = db.query(models.DriverLicense).filter(
        models.DriverLicense.id_doc == id_doc.id_doc)

    license_query.update(post, synchronize_session=False)
    db.commit()

    return license_query.first()
