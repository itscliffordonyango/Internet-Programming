"""
Obituary Management Platform - Main Application Entry Point.

This module initializes and configures the Flask application,
registers blueprints, sets up the database with automatic
schema migration, and configures error handlers.
"""

import os
from flask import Flask, render_template
from config import config
from sqlalchemy import inspect

# Import db from models to ensure proper initialization
from models.obituary import db
from routes.obituary_routes import obituary_bp
from routes.seo_routes import seo_bp


def upgrade_database_schema(app):
    """
    Automatically add missing columns to existing database tables.

    SQLAlchemy's db.create_all() does not alter existing tables.
    This helper checks if expected columns exist and adds them
    if missing, preventing "no such column" errors when the
    model is updated (e.g., adding image_filename).
    """
    with app.app_context():
        inspector = inspect(db.engine)
        # Expected model columns that may need to be added
        expected_columns = {
            "image_filename": "VARCHAR(255)",
        }
        existing_columns = [
            col["name"] for col in inspector.get_columns("obituaries")
        ]
        for col_name, col_type in expected_columns.items():
            if col_name not in existing_columns:
                with db.engine.connect() as conn:
                    conn.exec_driver_sql(
                        f"ALTER TABLE obituaries ADD COLUMN {col_name} {col_type}"
                    )
                    conn.commit()
                    app.logger.info(
                        f"Added missing column '{col_name}' to obituaries table"
                    )


def create_app(config_name=None):
    """
    Application factory function.

    Creates and configures a Flask application instance.

    Args:
        config_name: The configuration environment to use.
                     Defaults to 'development' if not specified.

    Returns:
        A configured Flask application instance.
    """
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "default")

    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config["default"]))

    # Ensure the database directory exists (required for SQLite)
    db_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    if db_uri.startswith("sqlite"):
        db_path = db_uri.replace("sqlite:///", "")
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

    # Initialize database
    db.init_app(app)

    # Create database tables and run schema migration
    with app.app_context():
        db.create_all()
        upgrade_database_schema(app)

    # Register blueprints
    app.register_blueprint(obituary_bp)
    app.register_blueprint(seo_bp)

    # Register error handlers
    register_error_handlers(app)

    # Inject current year into all templates
    @app.context_processor
    def inject_current_year():
        """Inject the current year into all templates for the footer."""
        from datetime import datetime
        return {"current_year": datetime.now().year}

    return app


def register_error_handlers(app):
    """Register custom error handlers for the application."""

    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 Not Found errors."""
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 Internal Server errors."""
        db.session.rollback()
        return render_template("500.html"), 500


# Create the application instance
app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
