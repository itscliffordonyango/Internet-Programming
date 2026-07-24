"""
Configuration module for the Obituary Management Platform.

This module contains the application configuration classes,
including database URI, secret key, and other settings.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration class."""

    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"

    # Database configuration
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, 'database', 'obituary_platform.db')}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Application URL (used for SEO canonical URLs)
    APP_URL = os.environ.get("APP_URL") or "http://localhost:5000"

    # Pagination
    OBITUARIES_PER_PAGE = 6

    # Slug max length
    SLUG_MAX_LENGTH = 255

    # Name and author max length
    NAME_MAX_LENGTH = 100
    AUTHOR_MAX_LENGTH = 100

    # Minimum content length
    CONTENT_MIN_LENGTH = 10


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}

