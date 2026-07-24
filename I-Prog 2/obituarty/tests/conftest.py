"""
Pytest configuration and fixtures for the Obituary Management Platform tests.

This module defines the shared fixtures used across test files,
including the Flask test client and application context.
"""

import pytest
from app import create_app
from models.obituary import db as _db


@pytest.fixture
def app():
    """Create and configure a Flask application for testing."""
    application = create_app("testing")

    # Create all tables within the application context
    with application.app_context():
        _db.create_all()
        yield application
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client for the application."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test CLI runner for the application."""
    return app.test_cli_runner()
