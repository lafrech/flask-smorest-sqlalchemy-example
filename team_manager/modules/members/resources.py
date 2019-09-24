"""Members resources"""

from flask.views import MethodView

from team_manager.extensions.api import Blueprint, SQLCursorPage
from team_manager.extensions.database import db

from .models import Member
from .schemas import MemberSchema, MemberQueryArgsSchema


blp = Blueprint(
    'Members',
    __name__,
    url_prefix='/members',
    description="Operations on members"
)


@blp.route('/')
class Members(MethodView):

    @blp.etag
    @blp.arguments(MemberQueryArgsSchema, location='query')
    @blp.response(MemberSchema(many=True))
    @blp.paginate(SQLCursorPage)
    def get(self, args):
        """List members"""
        # TODO: Add birthdate min/max filters
        return db.session.query(Member).filter_by(**args)

    @blp.etag
    @blp.arguments(MemberSchema)
    @blp.response(MemberSchema, code=201)
    def post(self, new_item):
        """Add a new member"""
        item = Member(**new_item)
        db.session.add(item)
        db.session.commit()
        return item


@blp.route('/<uuid:item_id>')
class MembersById(MethodView):

    @blp.etag
    @blp.response(MemberSchema)
    def get(self, item_id):
        """Get member by ID"""
        return db.session.query(Member).get_or_404(item_id)

    @blp.etag
    @blp.arguments(MemberSchema)
    @blp.response(MemberSchema)
    def put(self, new_item, item_id):
        """Update an existing member"""
        item = db.session.query(Member).get_or_404(item_id)
        blp.check_etag(item, MemberSchema)
        MemberSchema().update(item, new_item)
        db.session.add(item)
        db.session.commit()
        return item

    @blp.etag
    @blp.response(code=204)
    def delete(self, item_id):
        """Delete a member"""
        item = db.session.query(Member).get_or_404(item_id)
        blp.check_etag(item, MemberSchema)
        db.session.delete(item)
        db.session.commit()
