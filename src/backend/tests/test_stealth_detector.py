from unittest.mock import MagicMock, patch
from Service.log_service import LogService

def test_detector_flags_mass_deletion():
    # 1. Setup the Repository and DB Mock
    mock_db = MagicMock()
    mock_repo = MagicMock()
    mock_repo.db = mock_db  # Link them so service.db works

    # 2. Mock the behavior: 6 deletions (triggers the threshold)
    mock_repo.count_recent_deletions.return_value = 6

    # 3. Mock the query chain to return None (user not yet in list)
    # We use 'return_value' on the final step of the chain
    mock_db.query.return_value.filter_by.return_value.first.return_value = None

    service = LogService(mock_repo)

    # 4. Act
    service.log_and_check(user_id=1, group_id="user", action="DELETED_STUFF")

    # 5. Assert: Check the DB mock directly
    assert mock_db.add.called
    assert mock_db.commit.called