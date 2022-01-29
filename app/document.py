from sqlalchemy.orm import Session

from app.db import models
from app.schemas import IdDoc


def create_document(db: Session, id_user: int, id_type: int, id_group: int):
    new_doc = models.Documents(id_user=id_user, id_type=id_type, id_group=id_group)
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    response = db.query(models.Documents).filter(models.Documents.id_user == id_user,
                                                 models.Documents.id_type == id_type).first()
    id_doc = IdDoc.from_orm(response)

    verify = models.Verifying(id_doc=id_doc.id_doc, id_status=1)
    db.add(verify)
    db.commit()
    db.refresh(verify)

    return id_doc


def get_document(db: Session, model, id_user: int, id_type: int):
    return db.query(model, models.VerifyingStatus.status) \
        .join(models.Documents, models.Documents.id_doc == model.id_doc) \
        .join(models.Verifying, models.Verifying.id_doc == models.Documents.id_doc) \
        .join(models.VerifyingStatus, models.VerifyingStatus.id_status == models.Verifying.id_status) \
        .filter(models.Documents.id_user == id_user, models.Documents.id_type == id_type).first()
