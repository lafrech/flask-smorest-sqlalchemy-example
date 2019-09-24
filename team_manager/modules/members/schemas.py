"""Members schema"""

import marshmallow as ma
from marshmallow_sqlalchemy import field_for

from team_manager.extensions.api import Schema, ModelSchema
from .models import Member


class MemberSchema(ModelSchema):
    id = field_for(Member, "id", dump_only=True)

    class Meta(ModelSchema.Meta):
        model = Member


class MemberQueryArgsSchema(Schema):
    first_name = ma.fields.Str()
    last_name = ma.fields.Str()
    # TODO: Add birthdate min/max filters
