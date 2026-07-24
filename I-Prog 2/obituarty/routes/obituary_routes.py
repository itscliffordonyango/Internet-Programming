"""
Obituary routes for the Obituary Management Platform.

This module defines all routes related to obituary CRUD operations,
including form submission, listing, searching, pagination, detail views,
and media upload handling.
"""

import os
import uuid
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from models.obituary import db, Obituary

obituary_bp = Blueprint("obituary", __name__)

# Allowed image file extensions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp", "bmp"}


def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_file(file):
    """
    Save an uploaded file to the uploads directory.

    Args:
        file: The uploaded file object from the request.

    Returns:
        The unique filename saved, or None if no valid file was provided.
    """
    if file and file.filename and file.filename.strip():
        if allowed_file(file.filename):
            # Generate a unique filename to prevent collisions
            original_ext = file.filename.rsplit(".", 1)[1].lower()
            unique_filename = f"{uuid.uuid4().hex}.{original_ext}"
            upload_folder = current_app.config.get(
                "UPLOAD_FOLDER",
                os.path.join(current_app.root_path, "static", "uploads"),
            )
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, unique_filename)
            file.save(file_path)
            return unique_filename
    return None


@obituary_bp.route("/")
def index():
    """Home page route."""
    return render_template("index.html")


@obituary_bp.route("/submit-obituary", methods=["GET", "POST"])
def submit_obituary():
    """
    Handle obituary submission.

    GET: Display the obituary submission form.
    POST: Validate and process the submitted obituary data including optional media upload.
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

    # Validate uploaded file (if provided)
    uploaded_file = request.files.get("image")
    file_error = None
    if uploaded_file and uploaded_file.filename and uploaded_file.filename.strip():
        if not allowed_file(uploaded_file.filename):
            file_error = "Image file must be one of: PNG, JPG, JPEG, GIF, WebP, or BMP."
            errors.append(file_error)

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

        # Save the uploaded image file (if any)
        image_filename = save_uploaded_file(uploaded_file)

        # Create new obituary record
        obituary = Obituary(
            name=name,
            date_of_birth=dob,
            date_of_death=dod,
            content=content,
            author=author,
            slug=slug,
            image_filename=image_filename,
        )

        db.session.add(obituary)
        db.session.commit()

        flash("Obituary submitted successfully.", "success")
        return redirect(url_for("obituary.obituary_detail", slug=slug))

    except Exception as e:
        db.session.rollback()
        # Log the error server-side
        current_app.logger.error(f"Database error during obituary submission: {str(e)}")
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
    app_url = current_app.config.get("APP_URL", "http://localhost:5000")
    canonical_url = f"{app_url}/obituary/{slug}"

    # Build image URL for social sharing
    if obituary.has_image():
        og_image = f"{app_url}/static/uploads/{obituary.image_filename}"
    else:
        og_image = f"{app_url}/static/images/default-obituary-image.svg"

    return render_template(
        "obituary_detail.html",
        obituary=obituary,
        meta_description=meta_description,
        keywords=keywords,
        canonical_url=canonical_url,
        app_url=app_url,
        og_image=og_image,
    )
