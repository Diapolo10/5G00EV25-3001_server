"""Unit tests for miscellaneous database functionality"""

from eguivalet_server.database import get_db


def test_get_db():
    """Tests getting a database connection"""

    db_iter = get_db()

    # The loop ensures the session gets closed
    for db in db_iter:
        assert not db.flush()
