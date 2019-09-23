"""Team Manager server application"""

from flask import Flask

from team_manager import extensions, modules
from team_manager.default_settings import DefaultConfig


def create_app():
    """Create application"""
    app = Flask('Team manager')

    app.config.from_object(DefaultConfig)
    # Override config with optional settings file
    app.config.from_envvar('FLASK_SETTINGS_FILE', silent=True)

    api = extensions.create_api(app)
    modules.register_blueprints(api)

    return app
