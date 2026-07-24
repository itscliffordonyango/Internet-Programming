"""
Obituary routes for the Obituary Management Platform.

This module defines all routes related to obituary CRUD operations,
including form submission, listing, searching, pagination, and detail views.
"""

from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from models.obituary import db, Obituary

obituary_bp = Blueprint("obituary", __name__)


@obituary_bp.route("/")
def index():
    """Home page route."""
    return render_template("index.html")


@obituary_bp.route("/submit-obituary", methods=["GET", "POST"])
def submit_obituary():
    """
    Handle obituary submission.

    GET: Display the obituary submission form.
    POST: Validate and process the submitted obituary data.
    """
    if request.method == "GET":
        return render_template("obituary_form.html")

    # POST request: process form submission
    name = request.form.get("name", "").strip()
    date_of_birth = request.form.get("date_of_birth", "").strip()
    date_of_death = request.form.get("date_of_death", "").strip()
    content = request.form.get("content", "").strip()
    author = request.form.get("author", "").strip()

    # --- Backend Validation ---
    errors = []

    # Validate name
    if not name:
        errors.append("Full name is required.")
    elif len(name) > 100:
        errors.append("Name must not exceed 100 characters.")

    # Validate author
    if not author:
        errors.append("Author name is required.")
    elif len(author) > 100:
        errors.append("Author name must not exceed 100 characters.")

    # Validate dates
    if not date_of_birth:
        errors.append("Date of birth is required.")
    if not date_of_death:
        errors.append("Date of death is required.")

    # Parse and validate date formats
    dob = None
    dod = None
    date_format = "%Y-%m-%d"

    if date_of_birth:
        try:
            dob = datetime.strptime(date_of_birth, date_format).date()
        except ValueError:
            errors.append("Date of birth must be in YYYY-MM-DD format.")

    if date_of_death:
        try:
            dod = datetime.strptime(date_of_death, date_format).date()
        except ValueError:
            errors.append("Date of death must be in YYYY-MM-DD format.")

    # Validate date logic (death date not before birth date)
    if dob and dod and dod < dob:
        errors.append("Date of death cannot be earlier than date of birth.")

    # Validate content
    if not content:
        errors.append("Obituary content is required.")
    elif len(content) < 10:
        errors.append("Obituary content must be at least 10 characters long.")

    # If there are validation errors, re-render the form with errors
    if errors:
        return render_template(
            "obituary_form.html",
            errors=errors,
            form_data={
                "name": name,
                "date_of_birth": date_of_birth,
                "date_of_death": date_of_death,
                "content": content,
                "author": author,
            },
        )

    # --- Process valid submission ---
    try:
        # Generate a unique slug
        slug = Obituary.generate_unique_slug(name)

        # Create new obituary record
        obituary = Obituary(
            name=name,
            date_of_birth=dob,
            date_of_death=dod,
            content=content,
            author=author,
            slug=slug,
        )

        db.session.add(obituary)
        db.session.commit()

        flash("Obituary submitted successfully.", "success")
        return redirect(url_for("obituary.obituary_detail", slug=slug))

    except Exception as e:
        db.session.rollback()
        # Log the error server-side (in production, use proper logging)
        app = __import__("flask").current_app
        app.logger.error(f"Database error during obituary submission: {str(e)}")
        flash(
            "An unexpected error occurred while submitting the obituary. "
            "Please try again later.",
            "error",
        )
        return render_template(
            "obituary_form.html",
            errors=["A database error occurred. Please try again."],
            form_data={
                "name": name,
                "date_of_birth": date_of_birth,
                "date_of_death": date_of_death,
                "content": content,
                "author": author,
            },
        )


@obituary_bp.route("/obituaries")
def view_obituaries():
    """
    Display all obituaries with search and pagination.

    Query parameters:
        page (int): Current page number (default: 1).
        search (str): Optional search term to filter obituaries.
    """
    page = request.args.get("page", 1, type=int)
    search_query = request.args.get("search", "").strip()

    # Build base query
    query = Obituary.query.order_by(Obituary.submission_date.desc())

    # Apply search filter if provided
    if search_query:
        search_term = f"%{search_query}%"
        query = query.filter(
            db.or_(
                Obituary.name.ilike(search_term),
                Obituary.author.ilike(search_term),
                Obituary.content.ilike(search_term),
            )
        )

    # Paginate results
    pagination = query.paginate(
        page=page, per_page=6, error_out=False
    )

    obituaries = pagination.items

    return render_template(
        "view_obituaries.html",
        obituaries=obituaries,
        pagination=pagination,
        search_query=search_query,
    )


@obituary_bp.route("/obituary/<slug>")
def obituary_detail(slug):
    """
    Display individual obituary details.

    Args:
        slug: The unique URL-friendly slug for the obituary.
    """
    obituary = Obituary.query.filter_by(slug=slug).first_or_404()

    # Generate meta description from obituary content
    meta_description = (
        f"Remembering {obituary.name}. "
        f"{obituary.content[:150]}..."
        if len(obituary.content) > 150
        else f"Remembering {obituary.name}. {obituary.content}"
    )

    # Generate keywords
    keywords = (
        f"{obituary.name}, obituary, memorial, remembering, "
        f"in memory of, {obituary.author}"
    )

    # Get application URL for canonical and social tags
    from flask import current_app
    app_url = current_app.config.get("APP_URL", "http://localhost:5000")
    canonical_url = f"{app_url}/obituary/{slug}"

    return render_template(
        "obituary_detail.html",
        obituary=obituary,
        meta_description=meta_description,
        keywords=keywords,
        canonical_url=canonical_url,
        app_url=app_url,
    )

