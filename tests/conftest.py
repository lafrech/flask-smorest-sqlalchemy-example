import pytest

from team_manager import create_app


@pytest.fixture
def app():
    application = create_app()
    application.config['TESTING'] = True
    return application
