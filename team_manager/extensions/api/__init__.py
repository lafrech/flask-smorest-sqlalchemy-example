"""Api extension initialization

Override base classes here to allow painless customization in the future.
"""
from flask.views import MethodView
import marshmallow as ma
from marshmallow_sqlalchemy import TableSchema as OrigTableSchema

from flask_smorest import Api as ApiOrig, Blueprint as BlueprintOrig, Page

from team_manager.extensions.database import db


class Blueprint(BlueprintOrig):
    """Blueprint override"""

    def make_base_resource(blp, model, schema, query_args_schema):

        class BaseResource(MethodView):

            @blp.etag
            @blp.arguments(query_args_schema, location='query')
            @blp.response(schema(many=True))
            @blp.paginate(SQLCursorPage)
            def get(self, args):
                """List items"""
                # TODO: Add birthdate min/max filters
                return model.query.filter_by(**args)

            @blp.etag
            @blp.arguments(schema)
            @blp.response(schema, code=201)
            def post(self, new_item):
                """Add a new item"""
                item = model(**new_item)
                db.session.add(item)
                db.session.commit()
                return item

        return BaseResource

    def make_base_resource_by_id(blp, model, schema):

        class BaseResourceById(MethodView):

            @blp.etag
            @blp.response(schema)
            def get(self, item_id):
                """Get item by ID"""
                return model.query.get_or_404(item_id)

            @blp.etag
            @blp.arguments(schema)
            @blp.response(schema)
            def put(self, new_item, item_id):
                """Update an existing item"""
                item = model.query.get_or_404(item_id)
                blp.check_etag(item, schema)
                schema().update(item, new_item)
                db.session.add(item)
                db.session.commit()
                return item

            @blp.etag
            @blp.response(code=204)
            def delete(self, item_id):
                """Delete an item"""
                item = model.query.get_or_404(item_id)
                blp.check_etag(item, schema)
                db.session.delete(item)
                db.session.commit()

        return BaseResourceById


class Api(ApiOrig):
    """Api override"""

    def __init__(self, app=None, *, spec_kwargs=None):
        super().__init__(app, spec_kwargs=spec_kwargs)

        # Register custom Marshmallow fields in doc
        # self.register_field(CustomField, 'type', 'format')

        # Register custom Flask url parameter converters in doc
        # self.register_converter(CustomConverter, 'type', 'format')


class Schema(ma.Schema):
    """Schema override"""


class TableSchema(OrigTableSchema):
    """TableSchema override"""

    class Meta:
        include_fk = True

    def update(self, obj, data):
        """Update object nullifying missing data"""
        loadable_fields = [
            k for k, v in self.fields.items() if not v.dump_only
        ]
        for name in loadable_fields:
            setattr(obj, name, data.get(name))

    # FIXME: This does not respect allow_none fields
    @ma.post_dump
    def remove_none_values(self, data, **kwargs):
        return {
            key: value for key, value in data.items() if value is not None
        }


class SQLCursorPage(Page):
    """SQL cursor pager"""

    @property
    def item_count(self):
        return self.collection.count()
