"""Unit tests for user routes."""

import uuid

from fastapi import status

from eguivalet_server.config import (
    USER_ROOT as ROOT,
)


def test_post_new_user(client):
    """Tests creating new users."""
    data = {
        'username': "Finn McCool",
        'email': "finn.mccool@jmail.com",
        'password': "Tr0ub4dor&3",
    }

    response = client.post(f'{ROOT}/', json=data)
    assert response.status_code == status.HTTP_201_CREATED, response.text

    # Tests email match
    response = client.post(f'{ROOT}/', json=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text


def test_post_new_user_id_exists(client, test_users):
    """Tests creating a new user with an existing ID."""
    data = {
        'id': str(test_users[0]),
        'username': "Finn McCool",
        'email': "finn.mccool@jmail.com",
        'password': "Tr0ub4dor&3",
    }

    response = client.post(f'{ROOT}/', json=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text


def test_post_login_user(client, test_users):
    """Tests user login."""
    data = {
        'id': str(test_users[0]),
        'username': "Lazar Diarmaid",
        'email': "lazar.diarmaid@fian.na",
    }

    response = client.post(f'{ROOT}/login', json=data)
    assert response.status_code == status.HTTP_200_OK, response.text


def test_post_logout_user(client, test_users):
    """Tests user logout."""
    data = {
        'id': str(test_users[0]),
        'username': "Lazar Diarmaid",
        'email': "lazar.diarmaid@fian.na",
    }

    response = client.post(f'{ROOT}/logout', json=data)
    assert response.status_code == status.HTTP_200_OK, response.text


def test_get_user_by_id(client, test_users):
    """Tests getting users by ID."""
    response = client.get(f'{ROOT}/{test_users[0]}')
    assert response.status_code == status.HTTP_200_OK, response.text


def test_update_user_by_id(client, test_users):
    """Tests updating user information by ID."""
    data = {
        'id': str(test_users[0]),
        'username': "Lazar Diarmaid",
        'email': "lazar.diarmaid@fian.na",
    }

    response = client.put(f'{ROOT}/{test_users[0]}', json=data)
    assert response.status_code == status.HTTP_200_OK, response.text


def test_update_user_by_id_nonexistent(client):
    """Tests updating user information by ID when the user does not exist."""
    user_id = uuid.uuid4()

    data = {
        'id': str(user_id),
        'username': "Lazar Diarmaid",
        'email': "lazar.diarmaid@fian.na",
    }

    response = client.put(f'{ROOT}/{user_id}', json=data)
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text


def test_delete_user_by_id(client, test_users):
    """Tests deleting user by ID."""
    response = client.delete(f'{ROOT}/{test_users[0]}')
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.text

    response = client.get(f'{ROOT}/{test_users[0]}')
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
