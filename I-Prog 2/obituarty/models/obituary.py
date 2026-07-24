"""
This module defines the Obituary SQLAlchemy model representing
a deceased person's obituary record in the database.
"""

from datetime import datetime, date, timezone
from flask_sqlalchemy import SQLAlchemy
from slugify import slugify as generate_slug

db = SQLAlchemy()


class Obituary(db.Model):
    """
    Each obituary contains biographical information, the obituary text,
    author details, and a unique SEO-friendly slug for URL generation.
    Optionally includes a media image filename for uploaded photos.
    """

    __tablename__ = "obituaries"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    date_of_death = db.Column(db.Date, nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    submission_date = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    slug = db.Column(db.String(255), unique=True, nullable=False, index=True)
    image_filename = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        """Returning a string representation of the obituary record."""
        return (
            f"<Obituary(id={self.id}, name='{self.name}', "
            f"slug='{self.slug}', submission_date='{self.submission_date}')>"
        )

    def to_dict(self):
        """Converting the obituary record to a dictionary for templates."""
        return {
            "id": self.id,
            "name": self.name,
            "date_of_birth": self.date_of_birth,
            "date_of_death": self.date_of_death,
            "content": self.content,
            "author": self.author,
            "submission_date": self.submission_date,
            "slug": self.slug,
            "image_filename": self.image_filename,
        }

    def has_image(self):
        """Check if this obituary has an uploaded image."""
        return self.image_filename is not None and self.image_filename != ""

    @staticmethod
    def generate_unique_slug(name, existing_slug=None):
        """
        Generate a unique URL-friendly slug from the person's name.

        If an obituary with the same slug already exists, append a number
        to make it unique (e.g., 'john-kamau-2').
        This is to avoid duplicate data entry to the database

        Args:
            name: The full name of the deceased person.
            existing_slug: Optional slug to check uniqueness against.

        Returns:
            A unique slug string.
        """
        base_slug = generate_slug(name)
        slug = base_slug

        # Handle shorter names (minimum 3 chars for slug)
        if len(slug) < 3:
            slug = f"{slug}-obituary"

        # Ensure uniqueness by appending a counter if needed
        counter = 1
        query = Obituary.query.filter_by(slug=slug)
        if existing_slug:
            query = query.filter(Obituary.slug != existing_slug)

        while query.first() is not None:
            slug = f"{base_slug}-{counter}"
            if len(base_slug) < 3:
                slug = f"{base_slug}-obituary-{counter}"
            counter += 1
            query = Obituary.query.filter_by(slug=slug)
            if existing_slug:
                query = query.filter(Obituary.slug != existing_slug)

        return slug[:255]

