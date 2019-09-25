"""Teams schema"""

import marshmallow as ma
from marshmallow_sqlalchemy import field_for

from team_manager.extensions.api import Schema, ModelSchema
from team_manager.models.teams import Team


class TeamSchema(ModelSchema):
    id = field_for(Team, "id", dump_only=True)

    class Meta(ModelSchema.Meta):
        model = Team


class TeamQueryArgsSchema(Schema):
    name = ma.fields.Str()
    member = ma.fields.Str()
