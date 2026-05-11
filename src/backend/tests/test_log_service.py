from unittest.mock import MagicMock
from Service.log_service import LogService


def test_stealth_detector_flags_user():
    mock_db = MagicMock()
    mock_db.query.return_value.filter_by.return_value.first.return_value = None

    mock_repo = MagicMock()
    mock_repo.db = mock_db
    mock_repo.count_recent_deletions.return_value = 6

    service = LogService(mock_repo)
    service.log_and_check(user_id=1, group_id="user", action="DELETED_STUFF")

    assert mock_db.add.called