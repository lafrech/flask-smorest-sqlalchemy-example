"""Members model"""

import uuid

import sqlalchemy as sa
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils.types.uuid import UUIDType

from team_manager.extensions.database import db


class Member(db.Model):
    """Member model class"""
    __tablename__ = "members"

    id = sa.Column(UUIDType, primary_key=True, default=uuid.uuid4)
    first_name = sa.Column(sa.String(length=40))
    last_name = sa.Column(sa.String(length=40))
    birthdate = sa.Column(sa.DateTime)
    team_id = sa.Column(UUIDType, sa.ForeignKey("teams.id"))
    team = relationship("Team", backref=backref("members"))
