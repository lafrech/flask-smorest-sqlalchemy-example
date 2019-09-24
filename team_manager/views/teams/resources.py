"""Teams resources"""

from flask.views import MethodView

from team_manager.extensions.api import Blueprint, SQLCursorPage
from team_manager.extensions.database import db
from team_manager.models import Team

from .schemas import TeamSchema, TeamQueryArgsSchema


blp = Blueprint(
    'Teams',
    __name__,
    url_prefix='/teams',
    description="Operations on teams"
)


@blp.route('/')
class Teams(MethodView):

    @blp.etag
    @blp.arguments(TeamQueryArgsSchema, location='query')
    @blp.response(TeamSchema(many=True))
    @blp.paginate(SQLCursorPage)
    def get(self, args):
        """List teams"""
        # TODO: Add member filters
        return db.session.query(Team).filter_by(**args)

    @blp.etag
    @blp.arguments(TeamSchema)
    @blp.response(TeamSchema, code=201)
    def post(self, new_item):
        """Add a new team"""
        item = Team(**new_item)
        db.session.add(item)
        db.session.commit()
        return item


@blp.route('/<uuid:item_id>')
class TeamsById(MethodView):

    @blp.etag
    @blp.response(TeamSchema)
    def get(self, item_id):
        """Get team by ID"""
        return db.session.query(Team).get_or_404(item_id)

    @blp.etag
    @blp.arguments(TeamSchema)
    @blp.response(TeamSchema)
    def put(self, new_item, item_id):
        """Update an existing team"""
        item = db.session.query(Team).get_or_404(item_id)
        blp.check_etag(item, TeamSchema)
        TeamSchema().update(item, new_item)
        db.session.add(item)
        db.session.commit()
        return item

    @blp.etag
    @blp.response(code=204)
    def delete(self, item_id):
        """Delete a team"""
        item = db.session.query(Team).get_or_404(item_id)
        blp.check_etag(item, TeamSchema)
        db.session.delete(item)
        db.session.commit()
