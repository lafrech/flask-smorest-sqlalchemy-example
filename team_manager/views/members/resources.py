"""Members resources"""

from team_manager.extensions.api import Blueprint
from team_manager.models import Member

from .schemas import MemberSchema, MemberQueryArgsSchema


blp = Blueprint(
    'Members',
    __name__,
    url_prefix='/members',
    description="Operations on members"
)


BaseResource = blp.make_base_resource(
    Member, MemberSchema, MemberQueryArgsSchema)

@blp.route('/')
class Members(BaseResource):
    pass


BaseResourceById = blp.make_base_resource_by_id(Member, MemberSchema)

@blp.route('/<uuid:item_id>')
class MembersById(BaseResourceById):
    pass
