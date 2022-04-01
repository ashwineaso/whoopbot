import uuid

from sqlalchemy import (
    CHAR,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    TypeDecorator
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import current_timestamp

from whoopbot.db import Base


class GUID(TypeDecorator):
    """
    Platform independent GUID type uses CHAR(32) stored as string hex values.
    """

    impl = CHAR

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        if not isinstance(value, uuid.UUID):
            return "%.32x" % uuid.UUID(value).int
        return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if not isinstance(value, uuid.UUID):
            value = uuid.UUID(value)
        return value


class OrgResources(Base):
    """
    Table of resources for an organization.
    """

    __tablename__ = 'org_resources'

    id = Column(GUID(), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    resource_name = Column(String(255), nullable=False)
    environment = Column(String(255), nullable=True)


class LockedResource(Base):
    """
    Table of locked resources for an organization.
    """

    __tablename__ = 'locked_resources'

    id = Column(Integer, primary_key=True, index=True)
    resource_id = Column(GUID(), ForeignKey('org_resources.id'),
                         nullable=False, index=True)
    locked_at = Column(DateTime, nullable=False, default=current_timestamp())
    expires_at = Column(DateTime, nullable=False)

    resource = relationship('OrgResources', backref='locked_resources')

