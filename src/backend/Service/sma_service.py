from typing import List, Dict, Any, Optional
from Repository.review_repository import ReviewRepository
from Repository.sma_repository import SMARepository
from Domain.models.SMA import SMAModel


class SMAService:
    def __init__(self, sma_repo: SMARepository, review_repo: ReviewRepository):
        self.sma_repo = sma_repo
        self.review_repo = review_repo

    def get_all_movies(self) -> List[SMAModel]:
        return self.sma_repo.get_all()

    def get_movie_by_id(self, movie_id: int) -> Optional[SMAModel]:
        return self.sma_repo.get_by_id(movie_id)

    def get_paginated_movies(self, page: int, size: int) -> List[SMAModel]:
        return self.sma_repo.get_paginated(limit=size, offset=(page - 1) * size)

    def get_statistics(self,user_id) -> Dict[str, Any]:
        if not user_id:
            return {"total_reviews": 0, "rating_distribution": [], "type_distribution": []}

        stats_data = self.review_repo.get_stats_summary(user_id)

        return {
            "total_reviews": stats_data["total"],
            "rating_distribution": stats_data["ratings"],
            "type_distribution": stats_data["types"]
        }