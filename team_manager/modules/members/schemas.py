"""Members schema"""

import marshmallow as ma

from team_manager.extensions.api import Schema, ModelSchema
from .models import Member


class MemberSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Member


class MemberQueryArgsSchema(Schema):
    first_name = ma.fields.Str()
    last_name = ma.fields.Str()
    # TODO: Add birthdate min/max filters
