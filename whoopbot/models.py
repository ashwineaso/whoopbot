import os
from datetime import datetime

from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute

from whoopbot.db import Base


class OrgResource(Base):
    """
    Table of resources for an organization.
    """

    resource_name = UnicodeAttribute(hash_key=True)
    environment = UnicodeAttribute(range_key=True)

    def to_string(self):
        return f"{self.resource_name} - {self.environment}"

    class Meta:
        table_name = 'org_resources'
        region = os.getenv('AWS_REGION')


class LockedResource(Base):
    """
    Table of locked resources for an organization.
    """

    resource_name = UnicodeAttribute(hash_key=True)
    environment = UnicodeAttribute(range_key=True)
    owner_id = UnicodeAttribute()
    locked_at = UTCDateTimeAttribute(default=datetime.utcnow())
    expires_at = UTCDateTimeAttribute()

    class Meta:
        table_name = 'locked_resources'
        region = os.getenv('AWS_REGION')

