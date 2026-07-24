"""
Routes package for the Obituary Management Platform.

This package contains all route blueprints for the application.
"""

from routes.obituary_routes import obituary_bp
from routes.seo_routes import seo_bp

__all__ = ["obituary_bp", "seo_bp"]

