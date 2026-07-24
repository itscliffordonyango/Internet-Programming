"""
SEO routes for the Obituary Management Platform.

This module defines routes for SEO-related features including
the XML sitemap generation.
"""

from flask import Blueprint, Response, render_template
from models.obituary import Obituary

seo_bp = Blueprint("seo", __name__)


@seo_bp.route("/sitemap.xml")
def sitemap():
    """
    Generate an XML sitemap of the website.

    The sitemap includes:
    - Home page
    - Obituary listing page
    - Every individual obituary URL

    Returns:
        XML response with proper Content-Type header.
    """
    # Gather all obituaries for individual URLs
    obituaries = Obituary.query.order_by(Obituary.submission_date.desc()).all()

    # Build the list of pages
    pages = [
        {"loc": "/", "priority": "1.0", "changefreq": "daily"},
        {"loc": "/obituaries", "priority": "0.9", "changefreq": "daily"},
        {"loc": "/submit-obituary", "priority": "0.7", "changefreq": "monthly"},
    ]

    # Add individual obituary pages
    for obituary in obituaries:
        # Format the last modified date (submission date)
        lastmod = obituary.submission_date.strftime("%Y-%m-%d") if obituary.submission_date else ""
        pages.append({
            "loc": f"/obituary/{obituary.slug}",
            "priority": "0.8",
            "changefreq": "monthly",
            "lastmod": lastmod,
        })

    # Render XML template
    sitemap_xml = render_template("sitemap.xml", pages=pages)

    return Response(sitemap_xml, mimetype="application/xml")

