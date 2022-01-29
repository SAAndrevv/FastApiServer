from fastapi import status, HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from .. import schemas, oauth2
from ..db import models
from ..db.database import get_db
from ..document import create_document, get_document
from ..schemas import IdDoc

router = APIRouter(
    tags=["Mandatory health insurance"],
    prefix="/health_insurance"
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.MandatoryHealthInsurance)
def add_health_insurance(post: schemas.MandatoryHealthInsurance, db: Session = Depends(get_db),
                         current_user: schemas.UserToken = Depends(oauth2.get_current_user_data)):
    if current_user.role not in ["owner"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Access denied")

    document = db.query(models.Documents).filter(models.Documents.id_user == current_user.id_user,
                                                 models.Documents.id_type == 3).first()

    if document:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Health insurance license of user id {current_user.id_user} is already created")

    post = post.dict()
    post.pop("verifying")

    id_doc = create_document(db, current_user.id_user, 3, 1)
    new_insurance = models.MandatoryHealthInsurance(id_doc=id_doc.id_doc, **post)
    db.add(new_insurance)
    db.commit()
    db.refresh(new_insurance)
    #PASSPORT
    #DRIVER_LICENSE
    #MANDATORY_HEALTH_INSURANCE

    return new_insurance


@router.get("/", response_model=schemas.MandatoryHealthInsurance)
def get_health_insurance(db: Session = Depends(get_db),
                         current_user: schemas.UserToken = Depends(oauth2.get_current_user_data)):
    if current_user.role == "shared" and "MANDATORY_HEALTH_INSURANCE" not in current_user.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Access denied")

    insurance = get_document(db, models.MandatoryHealthInsurance, current_user.id_user, 3)

    if not insurance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Health insurance of user id {current_user.id_user} was not found")

    new_insurance = schemas.MandatoryHealthInsurance.from_orm(insurance[0])
    new_insurance.verifying = insurance[1]

    return new_insurance


@router.put("/", response_model=schemas.MandatoryHealthInsurance)
def update_health_insurance(post: schemas.MandatoryHealthInsurance, db: Session = Depends(get_db),
                            current_user: schemas.UserToken = Depends(oauth2.get_current_user_data)):
    if current_user.role not in ["owner"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Access denied")

    document = db.query(models.Documents).filter(models.Documents.id_user == current_user.id_user,
                                                 models.Documents.id_type == 3).first()

    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Health insurance of user id {current_user.id_user} does not exist")

    id_doc = IdDoc.from_orm(document)
    post = post.dict()
    post.pop("verifying")

    insurance = db.query(models.MandatoryHealthInsurance).filter(
        models.MandatoryHealthInsurance.id_doc == id_doc.id_doc)

    insurance.update(post, synchronize_session=False)
    db.commit()

    return insurance.first()
