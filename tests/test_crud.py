"""Tests for CRUD-operations not tested elsewhere"""

from server import crud

def test_read_public_rooms_all(db_session, public_rooms):
    """Tests fetching all public rooms"""

    db_rooms = crud.read_public_rooms(db_session)
    assert len(db_rooms) == len(public_rooms), db_rooms
    assert {
        room.id
        for room in db_rooms
    } == set(public_rooms), (db_rooms, public_rooms)


def test_read_users_all(db_session, test_users):
    """Tests fetching all users"""

    db_users = crud.read_users(db_session)
    assert len(db_users) == len(test_users), db_users
    assert {
        user.id
        for user in db_users
    } == set(test_users), (db_users, test_users)


def test_read_users_first_only(db_session, test_users):
    """Test fetching only the first user"""

    db_users = crud.read_users(db_session, limit=1)
    assert len(db_users) == 1, db_users
    assert db_users[0].id == test_users[0]


def test_read_users_slice(db_session, test_users):
    """Test fetching a slice of users"""

    db_users = crud.read_users(db_session, skip=1, limit=3)
    assert len(db_users) == 3, db_users
    assert {
        user.id
        for user in db_users
    } == set(test_users[1:4]), (db_users, test_users[1:4])
