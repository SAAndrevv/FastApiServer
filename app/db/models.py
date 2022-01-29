from sqlalchemy import Column, Integer, String, text, TIMESTAMP, ForeignKey

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id_user = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class Passport(Base):
    __tablename__ = "passport"

    id = Column(Integer, primary_key=True, nullable=False)
    type = Column(String, nullable=False)
    serial_and_number = Column(String, nullable=False)
    place_of_birth = Column(String, nullable=False)
    date_of_receiving = Column(String, nullable=False)
    issued_by = Column(String, nullable=False)
    department_code = Column(String, nullable=False)
    id_doc = Column(Integer, ForeignKey("documents.id_doc", ondelete="CASCADE"), nullable=False)


class DriverLicense(Base):
    __tablename__ = "driver_license"

    id = Column(Integer, primary_key=True, nullable=False)
    serial_and_number = Column(String, nullable=False)
    date_of_issue = Column(String, nullable=False)
    valid_until = Column(String, nullable=False)
    id_doc = Column(Integer, ForeignKey("documents.id_doc", ondelete="CASCADE"), nullable=False)


class MandatoryHealthInsurance(Base):
    __tablename__ = "mandatory_health_insurance"

    id = Column(Integer, primary_key=True, nullable=False)
    number = Column(String, nullable=False)
    valid_until = Column(String, nullable=True)
    id_doc = Column(Integer, ForeignKey("documents.id_doc", ondelete="CASCADE"), nullable=False)


class InsuranceNumberOfAnIndividualPersonAccount(Base):
    __tablename__ = "insurance_number_of_an_individual_person_account"

    id = Column(Integer, primary_key=True, nullable=False)
    number = Column(String, nullable=False)
    id_doc = Column(Integer, ForeignKey("documents.id_doc", ondelete="CASCADE"), nullable=False)


class Documents(Base):
    __tablename__ = "documents"

    id_doc = Column(Integer, primary_key=True, nullable=False)
    id_user = Column(Integer, ForeignKey("users.id_user", ondelete="CASCADE"), nullable=False)
    id_type = Column(Integer, ForeignKey("document_type.id_type"), nullable=False)
    id_group = Column(Integer, ForeignKey("document_group.id_group"), nullable=False)


class DocumentType(Base):
    __tablename__ = "document_type"

    id_type = Column(Integer, primary_key=True, nullable=False)
    doc_type = Column(String, nullable=False)


class DocumentGroup(Base):
    __tablename__ = "document_group"

    id_group = Column(Integer, primary_key=True, nullable=False)
    doc_group = Column(String, nullable=False)


class Verifying(Base):
    __tablename__ = "verifying"

    id_verify = Column(Integer, primary_key=True, nullable=False)
    id_status = Column(Integer, ForeignKey("verifying_status.id_status"), nullable=False)
    id_doc = Column(Integer, ForeignKey("documents.id_doc"), nullable=False)


class VerifyingStatus(Base):
    __tablename__ = "verifying_status"

    id_status = Column(Integer, primary_key=True, nullable=False)
    status = Column(String, nullable=False)
