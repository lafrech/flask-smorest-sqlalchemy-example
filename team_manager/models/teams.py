"""Teams model"""

import uuid

import sqlalchemy as sa
from sqlalchemy_utils.types.uuid import UUIDType

from team_manager.extensions.database import db


class Team(db.Model):
    """Team model class"""
    __tablename__ = "teams"

    id = sa.Column(UUIDType, primary_key=True, default=uuid.uuid4)
    name = sa.Column(sa.String(length=40))
