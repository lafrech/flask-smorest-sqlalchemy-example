"""Teams resources"""

from team_manager.extensions.api import Blueprint, SQLCursorPage
from team_manager.models import Team, Member

from .schemas import TeamSchema, TeamQueryArgsSchema


blp = Blueprint(
    'Teams',
    __name__,
    url_prefix='/teams',
    description="Operations on teams"
)


BaseResource = blp.make_base_resource(
    Team, TeamSchema, TeamQueryArgsSchema)

@blp.route('/')
class Teams(BaseResource):

    @blp.etag
    @blp.arguments(TeamQueryArgsSchema, location='query')
    @blp.response(TeamSchema(many=True))
    @blp.paginate(SQLCursorPage)
    def get(self, args):
        """List teams"""
        member_id = args.pop('member_id', None)
        ret = Team.query.filter_by(**args)
        if member_id is not None:
            ret = ret.join(Team.members).filter(Member.id == member_id)
        return ret


BaseResourceById = blp.make_base_resource_by_id(Team, TeamSchema)

@blp.route('/<uuid:item_id>')
class TeamsById(BaseResourceById):
    pass
