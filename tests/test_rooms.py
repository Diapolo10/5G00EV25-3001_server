from fastapi import status

from server.config import (
    ROOM_ROOT as ROOT,
    TEST_UUIDS
)

def test_get_public_rooms(client):
    """Tests getting public chatrooms"""

    response = client.get(f'{ROOT}/')
    assert response.status_code == status.HTTP_200_OK, response.text
    print(response.json())


def test_post_new_room_public(client):
    """Test creating a new public room"""

    data = {
        'id': str(TEST_UUIDS[0]),
        'name': "Test Room",
        'public': True
    }

    response = client.post(f'{ROOT}/', json=data)
    assert response.status_code == status.HTTP_200_OK, response.text

    # We shouldn't be able to make the same room twice
    response = client.post(f'{ROOT}/', json=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text

    
