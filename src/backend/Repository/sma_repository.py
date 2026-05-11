from typing import List, Optional
from sqlalchemy.orm import Session
from Domain.models.SMA import SMAModel
from sqlalchemy import select

class SMARepository():
    def __init__(self, db : Session):
        self.db = db

    def get_all(self) -> List[SMAModel]:
        result = self.db.execute(select(SMAModel)).scalars().all()
        return list(result)

    def get_by_id(self, sma_id: int) -> Optional[SMAModel]:
        return self.db.query(SMAModel).filter_by(id=sma_id).first()

    def add(self, sma: SMAModel) -> SMAModel:
        self.db.add(sma)
        self.db.commit()
        self.db.refresh(sma)
        return sma

    def update(self, sma_id: int, updated_sma: SMAModel) -> Optional[SMAModel]:
        db_sma = self.get_by_id(sma_id)
        if db_sma:
            db_sma.name = updated_sma.name
            db_sma.duration = updated_sma.duration
            db_sma.year_released = updated_sma.year_released
            db_sma.image = updated_sma.image
            db_sma.type  = updated_sma.type
            db_sma.description = updated_sma.description

            self.db.commit()
            self.db.refresh(db_sma)
        return db_sma

    def delete(self, sma_id: int) -> bool:
        db_sma = self.get_by_id(sma_id)
        if db_sma:
            self.db.delete(db_sma)
            self.db.commit()
            return True
        return False

    def get_paginated(self, limit: int, offset: int):
        return self.db.query(SMAModel).offset(offset).limit(limit).all()

    def update_stats(self, sma_id: int, new_rating: float, new_count: int):
        self.db.query(SMAModel).filter_by(id=sma_id).update({
            "rating": new_rating,
            "number_of_reviews": new_count
        })
        self.db.commit()