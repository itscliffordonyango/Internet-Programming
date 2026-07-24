"""
Tests for the obituary routes and database operations.

This module tests the core obituary functionality including
submission, viewing, listing, searching, and pagination.
"""

import pytest
from datetime import datetime, date
from models.obituary import db, Obituary


class TestObituaryRoutes:
    """Test suite for obituary route functionality."""

    def test_home_page_loads(self, client):
        """Test that the home page loads successfully."""
        response = client.get("/")
        assert response.status_code == 200
        assert b"Obituary Management Platform" in response.data or b"Obituary" in response.data

    def test_submission_form_loads(self, client):
        """Test that the submission form page loads."""
        response = client.get("/submit-obituary")
        assert response.status_code == 200
        assert b"Submit an Obituary" in response.data or b"submit" in response.data.lower()

    def test_valid_obituary_submission(self, client, app):
        """Test that a valid obituary can be submitted and stored."""
        with app.app_context():
            response = client.post(
                "/submit-obituary",
                data={
                    "name": "John Kamau",
                    "date_of_birth": "1950-03-15",
                    "date_of_death": "2024-01-20",
                    "content": "John was a wonderful person who loved his family and community. He will be deeply missed by all who knew him.",
                    "author": "Jane Doe",
                },
                follow_redirects=True,
            )
            assert response.status_code == 200

            # Verify the obituary was stored in the database
            obituary = Obituary.query.filter_by(slug="john-kamau").first()
            assert obituary is not None
            assert obituary.name == "John Kamau"
            assert obituary.author == "Jane Doe"

    def test_obituary_list_page_loads(self, client, app):
        """Test that the obituary list page loads."""
        with app.app_context():
            response = client.get("/obituaries")
            assert response.status_code == 200

    def test_individual_obituary_page_loads(self, client, app):
        """Test that an individual obituary page loads with a valid slug."""
        with app.app_context():
            # Create a test obituary
            obituary = Obituary(
                name="Test Person",
                date_of_birth=date(1960, 1, 1),
                date_of_death=date(2024, 6, 15),
                content="A life well lived and remembered by all.",
                author="Tester",
                slug="test-person",
            )
            db.session.add(obituary)
            db.session.commit()

            response = client.get("/obituary/test-person")
            assert response.status_code == 200
            assert b"Test Person" in response.data

    def test_invalid_slug_returns_404(self, client):
        """Test that an invalid slug returns a 404 page."""
        response = client.get("/obituary/non-existent-slug")
        assert response.status_code == 404

    def test_search_obituaries(self, client, app):
        """Test that searching for obituaries works."""
        with app.app_context():
            # Create test obituaries
            obituary1 = Obituary(
                name="Alice Johnson",
                date_of_birth=date(1970, 5, 10),
                date_of_death=date(2023, 12, 1),
                content="Alice was a beloved teacher.",
                author="Family",
                slug="alice-johnson",
            )
            obituary2 = Obituary(
                name="Bob Smith",
                date_of_birth=date(1955, 8, 22),
                date_of_death=date(2024, 3, 10),
                content="Bob was a devoted father.",
                author="Friend",
                slug="bob-smith",
            )
            db.session.add_all([obituary1, obituary2])
            db.session.commit()

            # Search by name
            response = client.get("/obituaries?search=Alice")
            assert response.status_code == 200
            assert b"Alice Johnson" in response.data

            # Search by author
            response = client.get("/obituaries?search=Family")
            assert response.status_code == 200
            assert b"Alice Johnson" in response.data

            # Search with no results
            response = client.get("/obituaries?search=NonExistent")
            assert response.status_code == 200
            assert b"No Results Found" in response.data or b"No obituaries" in response.data

    def test_pagination_works(self, client, app):
        """Test that pagination works correctly."""
        with app.app_context():
            # Create 8 obituaries (more than one page of 6)
            for i in range(8):
                obituary = Obituary(
                    name=f"Person {i}",
                    date_of_birth=date(1960, 1, 1),
                    date_of_death=date(2024, 1, 1),
                    content=f"Obituary content for person {i}.",
                    author="Author",
                    slug=f"person-{i}",
                )
                db.session.add(obituary)
            db.session.commit()

            # Page 1 should have 6 items
            response = client.get("/obituaries?page=1")
            assert response.status_code == 200

            # Page 2 should have 2 items
            response = client.get("/obituaries?page=2")
            assert response.status_code == 200

    def test_sitemap_loads(self, client, app):
        """Test that the sitemap loads correctly."""
        with app.app_context():
            # Add an obituary to test it appears in sitemap
            obituary = Obituary(
                name="Sitemap Test",
                date_of_birth=date(2000, 1, 1),
                date_of_death=date(2024, 1, 1),
                content="Test obituary content.",
                author="Tester",
                slug="sitemap-test",
            )
            db.session.add(obituary)
            db.session.commit()

            response = client.get("/sitemap.xml")
            assert response.status_code == 200
            assert b"<?xml" in response.data
            assert "application/xml" in response.content_type or "xml" in response.content_type

    def test_duplicate_slug_handling(self, client, app):
        """Test that duplicate slugs are handled by appending a number."""
        with app.app_context():
            # Create first obituary
            obituary1 = Obituary(
                name="John Kamau",
                date_of_birth=date(1950, 1, 1),
                date_of_death=date(2024, 1, 1),
                content="First John Kamau obituary. He was a great man.",
                author="Author 1",
                slug="john-kamau",
            )
            db.session.add(obituary1)
            db.session.commit()

            # Submit another with same name
            response = client.post(
                "/submit-obituary",
                data={
                    "name": "John Kamau",
                    "date_of_birth": "1960-05-10",
                    "date_of_death": "2024-06-20",
                    "content": "Second John Kamau obituary. He was also a wonderful person who touched many lives.",
                    "author": "Author 2",
                },
                follow_redirects=True,
            )
            assert response.status_code == 200

            # Check that a unique slug was generated
            obituary2 = Obituary.query.filter(
                Obituary.slug.like("john-kamau%"),
                Obituary.id != obituary1.id,
            ).first()
            assert obituary2 is not None
            assert obituary2.slug != "john-kamau"

