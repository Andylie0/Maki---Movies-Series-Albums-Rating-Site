import strawberry
from typing import List, Optional

from pydantic import ConfigDict


@strawberry.type
class ReviewType:
    id: int
    movie_id: int
    text: str
    rating: float
    likes: int
    user_id: int

    @strawberry.field
    def movie(self, info: strawberry.Info) -> "SMAType":
        sma_service = info.context["sma_service"]
        return sma_service.sma_repo.get_by_id(self.movie_id)

@strawberry.type
class SMAType:
    id: int
    name: str
    number_of_reviews: int
    duration: int
    rating: float
    year_released: int
    image: str
    type: str
    description: str

    model_config = ConfigDict(from_attributes=True)

    @strawberry.field
    def media_type(self) -> str:
        return self.type.value if hasattr(self.type, 'value') else str(self.type)

    @strawberry.field
    def reviews(self, info: strawberry.Info) -> List[ReviewType]:
        review_service = info.context["review_service"]
        return review_service.review_repo.get_by_movie_id(self.id)


@strawberry.type
class PaginatedReviewType:
    items: List[ReviewType]
    total: int

@strawberry.type
class Query:
    @strawberry.field
    def get_reviews(self, info: strawberry.Info, page: int = 1, size: int = 7, user_id: Optional[int] = None) -> PaginatedReviewType:
        review_service = info.context["review_service"]
        items, total_count = review_service.get_paginated_reviews(page, size, user_id)
        return PaginatedReviewType(items=items, total=total_count)

    @strawberry.field
    def get_movie(self, info: strawberry.Info, id: int) -> Optional[SMAType]:
        sma_service = info.context["sma_service"]
        return sma_service.sma_repo.get_by_id(id)

    @strawberry.field
    def get_movies(self, info: strawberry.Info) -> List[SMAType]:
        sma_service = info.context["sma_service"]
        return sma_service.sma_repo.get_all()

schema = strawberry.Schema(query=Query)