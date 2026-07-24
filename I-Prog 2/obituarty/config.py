"""
Configuration module for the Obituary Management Platform.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration class."""

    SECRET_KEY = (
        os.environ.get("SECRET_KEY")
        or "dev-secret-key-change-in-production"
    )

    # Project root directory
    BASE_DIR = os.path.abspath(
        os.path.dirname(__file__)
    )

    # Ensure the database directory exists
    DATABASE_DIR = os.path.join(
        BASE_DIR,
        "database"
    )

    os.makedirs(
        DATABASE_DIR,
        exist_ok=True
    )

    # Always use an absolute SQLite path
    DATABASE_PATH = os.path.join(
        DATABASE_DIR,
        "obituary_platform.db"
    )

    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{DATABASE_PATH}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Application URL
    APP_URL = (
        os.environ.get("APP_URL")
        or "http://localhost:5000"
    )

    # Pagination
    OBITUARIES_PER_PAGE = 6

    # Slug max length
    SLUG_MAX_LENGTH = 255

    # Name and author max length
    NAME_MAX_LENGTH = 100
    AUTHOR_MAX_LENGTH = 100

    # Minimum content length
    CONTENT_MIN_LENGTH = 10

    # Media upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "static",
        "uploads"
    )

    ALLOWED_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg",
        "gif",
        "webp",
        "bmp",
    }


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///:memory:"
    )


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}