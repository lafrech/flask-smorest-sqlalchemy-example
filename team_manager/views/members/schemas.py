"""Members schema"""

import marshmallow as ma
from marshmallow_sqlalchemy import field_for

from team_manager.extensions.api import Schema, TableSchema
from team_manager.models.members import Member


class MemberSchema(TableSchema):
    id = field_for(Member, "id", dump_only=True)

    class Meta(TableSchema.Meta):
        table = Member.__table__


class MemberQueryArgsSchema(Schema):
    first_name = ma.fields.Str()
    last_name = ma.fields.Str()
    team_id = ma.fields.UUID()
    # TODO: Add birthdate min/max filters
