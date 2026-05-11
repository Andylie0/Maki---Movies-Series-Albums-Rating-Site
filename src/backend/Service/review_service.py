from typing import List, Optional, Tuple, Dict, Any
from Domain.models.Review import ReviewModel
from Repository.review_repository import ReviewRepository
from Repository.sma_repository import SMARepository
from Service.log_service import LogService


class ReviewService:
    def __init__(self, review_repo: ReviewRepository, sma_repo: SMARepository,
                 log_service: LogService, ws_manager):
        self.review_repo = review_repo
        self.sma_repo = sma_repo
        self.log_service = log_service
        self.ws_manager = ws_manager

    async def add_review(self, data: Dict[str, Any], user_id: int) -> ReviewModel:
        new_review = ReviewModel(**data, user_id=user_id)
        saved_review = self.review_repo.add(new_review)

        sma = self.sma_repo.get_by_id(saved_review.movie_id)
        if sma:
            new_count = sma.number_of_reviews + 1
            new_avg = (sma.number_of_reviews * sma.rating + saved_review.rating) / new_count

            self.sma_repo.update_stats(sma.id, round(new_avg, 2), new_count)

            self.log_service.log_and_check(
                user_id=user_id,
                group_id="user",
                action=f"CREATED_REVIEW_ID_{saved_review.id}_FOR_MOVIE_{sma.id}"
            )

            await self.ws_manager.broadcast({
                "type": "NEW_REVIEW",
                "message": f"New review added for {sma.name}",
                "movie_id": sma.id
            })

        return saved_review

    async def update_review(self, review_id: int, data: Dict[str, Any], user_id: int) -> Optional[ReviewModel]:
        existing = self.review_repo.get_by_id(review_id)
        if not existing:
            return None

        old_rating = existing.rating
        updated_review = self.review_repo.update(review_id, data)

        sma = self.sma_repo.get_by_id(updated_review.movie_id)
        if sma and updated_review:
            new_avg = (sma.number_of_reviews * sma.rating - old_rating + updated_review.rating) / sma.number_of_reviews
            self.sma_repo.update_stats(sma.id, round(new_avg, 2), sma.number_of_reviews)

            self.log_service.log_and_check(
                user_id=user_id,
                group_id="user",
                action=f"UPDATED_REVIEW_ID_{review_id}"
            )

            await self.ws_manager.broadcast({"type": "UPDATE_REVIEW", "movie_id": sma.id})

        return updated_review

    async def delete_review(self, review_id: int, user_id: int) -> bool:
        review = self.review_repo.get_by_id(review_id)
        if not review:
            return False

        sma = self.sma_repo.get_by_id(review.movie_id)
        rating_to_remove = review.rating
        success = self.review_repo.delete(review_id)

        if success and sma:
            self.log_service.log_and_check(
                user_id=user_id,
                group_id="user",
                action=f"DELETED_REVIEW_ID_{review_id}"
            )

            if sma.number_of_reviews <= 1:
                self.sma_repo.update_stats(sma.id, 0.0, 0)
            else:
                new_count = sma.number_of_reviews - 1
                new_avg = (sma.number_of_reviews * sma.rating - rating_to_remove) / new_count
                self.sma_repo.update_stats(sma.id, round(new_avg, 2), new_count)

            await self.ws_manager.broadcast({"type": "DELETE_REVIEW", "movie_id": sma.id})
        return success

    def get_paginated_reviews(self, page: int, size: int, user_id : int = None, search: str = "") -> Tuple[List[ReviewModel], int]:
        return self.review_repo.get_paginated_with_search(
            limit=size,
            offset=(page - 1) * size,
            user_id = user_id,
            search_query=search
        )