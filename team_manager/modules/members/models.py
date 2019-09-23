"""Members model"""

import uuid

import sqlalchemy as sa
from sqlalchemy_utils.types.uuid import UUIDType

from team_manager.extensions.database import db


class Member(db.Model):
    """Member model class"""

    id = sa.Column(UUIDType, primary_key=True, default=uuid.uuid4)
    first_name = sa.Column(sa.String(length=40))
    last_name = sa.Column(sa.String(length=40))
    birthdate = sa.Column(sa.DateTime)
