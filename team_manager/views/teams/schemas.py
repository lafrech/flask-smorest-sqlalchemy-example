"""Teams schema"""

import marshmallow as ma
from marshmallow_sqlalchemy import field_for

from team_manager.extensions.api import Schema, TableSchema
from team_manager.models.teams import Team


class TeamSchema(TableSchema):
    id = field_for(Team, "id", dump_only=True)

    class Meta(TableSchema.Meta):
        table = Team.__table__


class TeamQueryArgsSchema(Schema):
    name = ma.fields.Str()
    member = ma.fields.UUID()
