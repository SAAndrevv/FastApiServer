from typing import List

from fastapi import status, HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from .. import schemas, oauth2
from ..db import models
from ..db.database import get_db

router = APIRouter(
    tags=["Available Documents"],
    prefix="/available_doc"
)


@router.get("/", response_model=List[schemas.Document])
def get_available_documents(db: Session = Depends(get_db),
                            current_user: schemas.UserToken = Depends(oauth2.get_current_user_data)):

    if current_user.role == "shared":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Access denied")

    groups = db.query(models.Documents.id_group) \
        .filter(models.Documents.id_user == current_user.id_user) \
        .group_by(models.Documents.id_group).all()

    groups_schemas = []
    for group in groups:
        schema = schemas.Document.from_orm(group)

        types = db.query(models.DocumentType.doc_type) \
            .join(models.Documents, models.Documents.id_type == models.DocumentType.id_type)\
            .filter(models.Documents.id_user == current_user.id_user,
                    models.Documents.id_group == schema.id_group).all()

        types_array = []
        for typ in types:
            types_array.append(typ)

        schema.data = types_array
        groups_schemas.append(schema)

    return groups_schemas

