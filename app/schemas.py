from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserAccessData(BaseModel):
    data: Optional[List[str]] = None


class UserToken(BaseModel):
    id_user: int
    role: str
    data: Optional[List[str]] = None


class UserOut(BaseModel):
    id_user: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id_user: Optional[str] = None


class IdDoc(BaseModel):
    id_doc: int

    class Config:
        orm_mode = True


class Document(BaseModel):
    id_group: int
    data: List[Optional[dict]] = None

    class Config:
        orm_mode = True


class Passport(BaseModel):
    type: str
    serial_and_number: str
    place_of_birth: str
    date_of_receiving: str
    issued_by: str
    department_code: str
    verifying: Optional[str]

    class Config:
        orm_mode = True


class DriverLicense(BaseModel):
    serial_and_number: str
    date_of_issue: str
    valid_until: str
    verifying: Optional[str]

    class Config:
        orm_mode = True


class MandatoryHealthInsurance(BaseModel):
    number: str
    valid_until: Optional[int]
    verifying: Optional[str]

    class Config:
        orm_mode = True


class InsuranceNumberOfAnIndividualPersonAccount(BaseModel):
    number: str
    verifying: Optional[str]

    class Config:
        orm_mode = True


