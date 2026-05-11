from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from Domain.models.Review import ReviewModel
from sqlalchemy import func, select
from Domain.models.SMA import SMAModel

class ReviewRepository():
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[ReviewModel]:
        stmt = select(ReviewModel).order_by(ReviewModel.id)
        result = self.db.execute(stmt).scalars().all()
        return list(result)

    def get_by_id(self, review_id: int) -> Optional[ReviewModel]:
        return self.db.query(ReviewModel).filter_by(id=review_id).first()

    def get_by_movie_id(self, movie_id: int) -> List[ReviewModel]:
        stmt = select(ReviewModel).filter_by(movie_id=movie_id)
        result = self.db.execute(stmt).scalars().all()
        return list(result)

    def add(self, item):
        try:
            if isinstance(item, dict):
                item = ReviewModel(**item)
            self.db.add(item)
            self.db.commit()
            self.db.refresh(item)
            return item
        except SQLAlchemyError as e:
            self.db.rollback()
            print(f"Database error: {e}")
            raise e

    def update(self, review_id: int, data: dict):
        db_review = self.get_by_id(review_id)
        if not db_review:
            return None
        for key, value in data.items():
            setattr(db_review, key, value)
        self.db.commit()
        self.db.refresh(db_review)
        return db_review

    def delete(self, review_id: int) -> bool:
        db_review = self.get_by_id(review_id)
        if db_review:
            self.db.delete(db_review)
            self.db.commit()
            return True
        return False

    def get_stats_summary(self,user_id : int):
        total = self.db.query(func.count(ReviewModel.id)).filter_by(user_id = user_id).scalar()

        ratings = self.db.query(
            ReviewModel.rating,
            func.count(ReviewModel.id)
        ).filter_by(user_id = user_id).group_by(ReviewModel.rating).all()

        types = self.db.query(
            SMAModel.type,
            func.count(ReviewModel.id)
        ).join(ReviewModel).filter_by(user_id = user_id).group_by(SMAModel.type).all()

        return {
            "total": total,
            "ratings": [{"rating": r, "count": c} for r, c in ratings],
            "types": [{"name": t.value, "value": c} for t, c in types]
        }

    def get_paginated_with_search(self, limit: int, offset: int, user_id : int = None, search_query: str = ""):
        query = self.db.query(ReviewModel).order_by(ReviewModel.id)

        if user_id:
            query = query.filter_by(user_id = user_id)

        if search_query:
            query = query.join(SMAModel).filter(SMAModel.name.ilike(f"%{search_query}%"))

        total_count = query.count()
        items = query.offset(offset).limit(limit).all()

        return items, total_count