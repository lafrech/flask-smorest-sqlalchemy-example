"""Members schema"""

import marshmallow as ma
from marshmallow_sqlalchemy import ModelSchema

from team_manager.extensions.api import Schema
from .models import Member


class MemberSchema(ModelSchema):
    class Meta:
        model = Member


class MemberQueryArgsSchema(Schema):
    first_name = ma.fields.Str()
    last_name = ma.fields.Str()
    # TODO: Add birthdate min/max filters
