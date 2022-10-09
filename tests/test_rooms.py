"""Unit tests for chatrooms"""

import uuid

import pytest
from fastapi import status
from pydantic import ValidationError

from server.config import (
    ROOM_ROOT as ROOT,
)


def test_get_public_rooms(client):
    """Tests getting public chatrooms"""

    response = client.get(f'{ROOT}/')
    assert response.status_code == status.HTTP_200_OK, response.text
    print(response.json())


def test_post_new_room_public(client):
    """Test creating a new public room"""

    data = {
        'id': str(uuid.uuid4()),
        'name': "Test Room",
        'public': True,
    }

    response = client.post(f'{ROOT}/', json=data)
    assert response.status_code == status.HTTP_200_OK, response.text

    # We shouldn't be able to make the same room twice
    response = client.post(f'{ROOT}/', json=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text


def test_post_new_room_private(client, test_users):
    """Test creating a new private room"""

    data = {
        'id': str(uuid.uuid4()),
        'name': "Private Test Room",
        'public': False,
        'owner': str(test_users[0]),
    }

    response = client.post(f'{ROOT}/', json=data)
    assert response.status_code == status.HTTP_200_OK, response.text

    # We shouldn't be able to make the same room twice
    response = client.post(f'{ROOT}/', json=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text


def test_post_new_room_private_no_owner(client):
    """Test error handling when creating an ownerless private room"""

    data = {
        'id': str(uuid.uuid4()),
        'name': "Private Test Room",
        'public': False,
    }

    with pytest.raises(ValidationError):
        _ = client.post(f'{ROOT}/', json=data)


def test_get_room_by_id_public(client, public_rooms):
    """Test fetching a public room"""

    response = client.get(f'{ROOT}/{public_rooms[0]}')
    assert response.status_code == status.HTTP_200_OK, response.text


def test_get_room_by_id_private(client, private_rooms):
    """Test fetching a private room"""

    response = client.get(f'{ROOT}/{private_rooms[0]}')
    assert response.status_code == status.HTTP_200_OK, response.text


def test_get_room_by_id_nonexistent(client):
    """Test fetching a room that does not exist"""

    response = client.get(f'{ROOT}/{uuid.uuid4()}')
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text


def test_post_message_by_id(client, public_rooms, test_users):
    """Test sending a message to a public room"""

    data = {
        'id': str(uuid.uuid4()),
        'user_id': str(test_users[0]),
        'message': "Vincit qui se vincit.",
    }

    response = client.post(f'{ROOT}/{public_rooms[0]}', json=data)
    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json()['message'] == "Vincit qui se vincit."

    response = client.post(f'{ROOT}/{public_rooms[0]}', json=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_delete_room_by_id_public(client, public_rooms):
    """Test deleting a public room"""

    # NOTE: We need to check admin permissions first

    response = client.delete(f'{ROOT}/{public_rooms[0]}')
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.text

    response = client.get(f'{ROOT}/{public_rooms[0]}')
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text


def test_delete_room_by_id_private(client, private_rooms):
    """Test deleting private rooms"""

    # NOTE: We need to check the room owner matches the
    # currently logged in user, or an administrator

    response = client.delete(f'{ROOT}/{private_rooms[0]}')
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.text

    response = client.get(f'{ROOT}/{private_rooms[0]}')
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text


def test_get_message_by_id(client, public_rooms, test_users):
    """Test fetching a message from a public room"""

    message_id = str(uuid.uuid4())

    data = {
        'id': message_id,
        'user_id': str(test_users[0]),
        'message': "Vincit qui se vincit.",
    }

    response = client.post(f'{ROOT}/{public_rooms[0]}', json=data)
    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json()['message'] == "Vincit qui se vincit."

    response = client.get(f'{ROOT}/{public_rooms[0]}/message/{message_id}')
    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json()['message'] == "Vincit qui se vincit."


def test_put_message_by_id(client, public_rooms, test_users):
    """Test editing a message from a public room"""

    message_id = str(uuid.uuid4())

    data = {
        'id': message_id,
        'user_id': str(test_users[0]),
        'message': "Vincit qui se vincit.",
    }

    response = client.post(f'{ROOT}/{public_rooms[0]}', json=data)
    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json()['message'] == "Vincit qui se vincit."

    edit_data = {
        'id': message_id,
        'user_id': str(test_users[0]),
        'message': "What you are, I was; what I am, you will be.",
    }

    response = client.put(f'{ROOT}/{public_rooms[0]}/message/{message_id}', json=edit_data)
    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json()['message'] == "What you are, I was; what I am, you will be."

    response = client.get(f'{ROOT}/{public_rooms[0]}/message/{message_id}')
    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json()['message'] == "What you are, I was; what I am, you will be."


def test_delete_message_by_id(client, public_rooms, test_users):
    """Test deleting a message from a public room"""

    message_id = str(uuid.uuid4())

    data = {
        'id': message_id,
        'user_id': str(test_users[0]),
        'message': "Je crois en moi.",
    }

    response = client.post(f'{ROOT}/{public_rooms[0]}', json=data)
    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json()['message'] == "Je crois en moi."

    response = client.delete(f'{ROOT}/{public_rooms[0]}/message/{message_id}')
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.text

    response = client.get(f'{ROOT}/{public_rooms[0]}/message/{message_id}')
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
