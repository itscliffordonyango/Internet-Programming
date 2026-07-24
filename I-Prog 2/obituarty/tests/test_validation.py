"""
Tests for form validation and error handling.

This module tests the backend validation logic, error pages,
and graceful error handling behaviour.
"""

import pytest
from datetime import date
from models.obituary import db, Obituary


class TestFormValidation:
    """Test suite for form validation logic."""

    def test_empty_name(self, client):
        """Test that submitting with an empty name shows an error."""
        response = client.post(
            "/submit-obituary",
            data={
                "name": "",
                "date_of_birth": "1950-01-01",
                "date_of_death": "2024-01-01",
                "content": "A valid obituary content for testing purposes.",
                "author": "Valid Author",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Full name is required" in response.data

    def test_empty_author(self, client):
        """Test that submitting with an empty author shows an error."""
        response = client.post(
            "/submit-obituary",
            data={
                "name": "Test Person",
                "date_of_birth": "1950-01-01",
                "date_of_death": "2024-01-01",
                "content": "A valid obituary content for testing purposes.",
                "author": "",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Author name is required" in response.data

    def test_empty_content(self, client):
        """Test that submitting with empty content shows an error."""
        response = client.post(
            "/submit-obituary",
            data={
                "name": "Test Person",
                "date_of_birth": "1950-01-01",
                "date_of_death": "2024-01-01",
                "content": "",
                "author": "Valid Author",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Obituary content is required" in response.data

    def test_invalid_dates(self, client):
        """Test that invalid date formats are rejected."""
        response = client.post(
            "/submit-obituary",
            data={
                "name": "Test Person",
                "date_of_birth": "invalid-date",
                "date_of_death": "2024-01-01",
                "content": "A valid obituary content for testing purposes.",
                "author": "Valid Author",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"must be in YYYY-MM-DD format" in response.data

    def test_death_date_before_birth_date(self, client):
        """Test that death date cannot be before birth date."""
        response = client.post(
            "/submit-obituary",
            data={
                "name": "Test Person",
                "date_of_birth": "2024-01-01",
                "date_of_death": "2020-01-01",
                "content": "A valid obituary content for testing purposes.",
                "author": "Valid Author",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Date of death cannot be earlier" in response.data

    def test_excessively_long_name(self, client):
        """Test that names exceeding 100 characters are rejected."""
        long_name = "A" * 101
        response = client.post(
            "/submit-obituary",
            data={
                "name": long_name,
                "date_of_birth": "1950-01-01",
                "date_of_death": "2024-01-01",
                "content": "A valid obituary content for testing purposes.",
                "author": "Valid Author",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Name must not exceed 100 characters" in response.data

    def test_excessively_long_author(self, client):
        """Test that author names exceeding 100 characters are rejected."""
        long_author = "A" * 101
        response = client.post(
            "/submit-obituary",
            data={
                "name": "Test Person",
                "date_of_birth": "1950-01-01",
                "date_of_death": "2024-01-01",
                "content": "A valid obituary content for testing purposes.",
                "author": long_author,
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Author name must not exceed 100 characters" in response.data

    def test_short_content(self, client):
        """Test that content shorter than 10 characters is rejected."""
        response = client.post(
            "/submit-obituary",
            data={
                "name": "Test Person",
                "date_of_birth": "1950-01-01",
                "date_of_death": "2024-01-01",
                "content": "Short",
                "author": "Valid Author",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"at least 10 characters" in response.data

    def test_404_error_page(self, client):
        """Test that a 404 page is returned for non-existent routes."""
        response = client.get("/nonexistent-page")
        assert response.status_code == 404
        # Should render the custom 404 template, not a generic one
        assert b"Page Not Found" in response.data or b"404" in response.data

    def test_missing_date_fields(self, client):
        """Test that missing date fields show appropriate errors."""
        response = client.post(
            "/submit-obituary",
            data={
                "name": "Test Person",
                "date_of_birth": "",
                "date_of_death": "",
                "content": "A valid obituary content for testing purposes.",
                "author": "Valid Author",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Date of birth is required" in response.data
        assert b"Date of death is required" in response.data
