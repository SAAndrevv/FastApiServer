from fastapi import status, HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from .. import schemas, oauth2
from ..db import models
from ..db.database import get_db
from ..document import create_document, get_document
from ..schemas import IdDoc

router = APIRouter(
    tags=["Insurance number of an individual person account"],
    prefix="/insurance_number"
)


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=schemas.InsuranceNumberOfAnIndividualPersonAccount)
def add_insurance_number(post: schemas.InsuranceNumberOfAnIndividualPersonAccount, db: Session = Depends(get_db),
                         current_user: schemas.UserToken = Depends(oauth2.get_current_user_data)):
    if current_user.role not in ["owner"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Access denied")

    document = db.query(models.Documents).filter(models.Documents.id_user == current_user.id_user,
                                                 models.Documents.id_type == 4).first()

    if document:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Insurance number of user id {current_user.id_user} is already created")

    post = post.dict()
    post.pop("verifying")

    id_doc = create_document(db, current_user.id_user, 4, 1)
    new_insurance = models.InsuranceNumberOfAnIndividualPersonAccount(id_doc=id_doc.id_doc, **post)
    db.add(new_insurance)
    db.commit()
    db.refresh(new_insurance)

    return new_insurance


@router.get("/", response_model=schemas.InsuranceNumberOfAnIndividualPersonAccount)
def get_health_insurance(db: Session = Depends(get_db),
                         current_user: schemas.UserToken = Depends(oauth2.get_current_user_data)):
    if current_user.role == "shared" and "INSURANCE_NUMBER_OF_AN_INDIVIDUAL_PERSON_ACCOUNT" not in current_user.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Access denied")

    insurance = get_document(db, models.InsuranceNumberOfAnIndividualPersonAccount, current_user.id_user, 4)

    if not insurance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Insurance number of user id {current_user.id_user} was not found")

    new_insurance = schemas.InsuranceNumberOfAnIndividualPersonAccount.from_orm(insurance[0])
    new_insurance.verifying = insurance[1]

    return new_insurance


@router.put("/", response_model=schemas.InsuranceNumberOfAnIndividualPersonAccount)
def update_health_insurance(post: schemas.InsuranceNumberOfAnIndividualPersonAccount, db: Session = Depends(get_db),
                            current_user: schemas.UserToken = Depends(oauth2.get_current_user_data)):
    if current_user.role not in ["owner"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Access denied")

    document = db.query(models.Documents).filter(models.Documents.id_user == current_user.id_user,
                                                 models.Documents.id_type == 4).first()

    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Insurance number of user id {current_user.id_user} does not exist")

    id_doc = IdDoc.from_orm(document)
    post = post.dict()
    post.pop("verifying")

    insurance = db.query(models.InsuranceNumberOfAnIndividualPersonAccount).filter(
        models.InsuranceNumberOfAnIndividualPersonAccount.id_doc == id_doc.id_doc)

    insurance.update(post, synchronize_session=False)
    db.commit()

    return insurance.first()
