import pytest
from unittest.mock import MagicMock, AsyncMock
from Service.review_service import ReviewService
from Domain.models.Review import ReviewModel

@pytest.mark.asyncio
async def test_add_review_persists_and_logs():
    review_repo = MagicMock()
    sma_repo = MagicMock()
    mock_log_service = MagicMock()  # Use the service mock here too
    ws_manager = MagicMock()
    ws_manager.broadcast = AsyncMock()

    saved = MagicMock(id=1, movie_id=10, rating=4.0)
    review_repo.add.return_value = saved
    sma_repo.get_by_id.return_value = MagicMock(
        id=10, name="X", number_of_reviews=1, rating=5.0
    )

    service = ReviewService(review_repo, sma_repo, mock_log_service, ws_manager)
    result = await service.add_review({"movie_id": 10, "rating": 4.0}, user_id=1)

    # 4. Bronze Assertions: Persistence
    assert result is saved
    assert review_repo.add.called

    # 5. Gold Assertion: Stealth Detection
    assert mock_log_service.log_and_check.called

    # Ensure SMA stats were updated (Bronze logic)
    assert sma_repo.update_stats.called

@pytest.mark.asyncio
async def test_add_review_triggers_log():
    # 1. Setup Mocks
    review_repo = MagicMock()
    sma_repo = MagicMock()
    # This mock represents the LogService (with Stealth Logic)
    mock_log_service = MagicMock()
    ws_manager = MagicMock()
    ws_manager.broadcast = AsyncMock()

    saved = MagicMock(id=2, movie_id=20, rating=3.0)
    review_repo.add.return_value = saved
    sma_repo.get_by_id.return_value = MagicMock(
        id=20, name="Y", number_of_reviews=0, rating=0.0
    )

    # 2. Inject the Service Mock
    service = ReviewService(review_repo, sma_repo, mock_log_service, ws_manager)
    await service.add_review({"movie_id": 20, "rating": 3.0}, user_id=7)

    # 3. Assert: Check that the STEALTH logic was triggered
    mock_log_service.log_and_check.assert_called_once()
