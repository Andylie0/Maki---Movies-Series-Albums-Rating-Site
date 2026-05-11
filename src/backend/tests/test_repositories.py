from Repository.review_repository import ReviewRepository
from Domain.models.Review import ReviewModel


def test_review_repo_crud(db_session):
    repo = ReviewRepository(db_session)

    # Test Create: Ensure your repo.add is actually creating a ReviewModel instance
    # Pass only the fields the model expects
    review_data = {"movie_id": 1, "text": "Classic", "rating": 5, "likes" : 0, "user_id": 1}
    new_review = repo.add(review_data)

    assert new_review.id is not None
    assert isinstance(new_review, ReviewModel)  # Verify it's not a dict

    # Test Get
    fetched = repo.get_by_id(new_review.id)
    assert fetched.text == "Classic"

    # Test Delete
    repo.delete(new_review.id)
    db_session.commit()  # Ensure the transaction finishes
    assert repo.get_by_id(new_review.id) is None