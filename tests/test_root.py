"""Unit tests for the root routes."""

from fastapi import status


def test_get_root(client):
    """Tests the hello world response."""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json() == {"hello": "Hello, world!"}, response.json()


def test_get_robots_txt(client):
    """Tests getting the robots.txt data."""
    response = client.get("/robots.txt")
    assert response.status_code == status.HTTP_200_OK, response.text
