from fastapi import APIRouter, Depends, HTTPException
from typing import List

from Repository.review_repository import ReviewRepository
from Repository.sma_repository import SMARepository
from Service.sma_service import SMAService
from Domain.models.SMA import SMAModel
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/movies", tags=["Movies"])

def get_sma_service(db : Session = Depends(get_db)):
    return SMAService(sma_repo = SMARepository(db), review_repo = ReviewRepository(db))

@router.get("/", response_model=List[dict])
async def get_movies(page: int = 1, size: int = 7, service: SMAService = Depends(get_sma_service)):
    return service.get_paginated_movies(page, size)

@router.get("/statistics")
def get_stats(service: SMAService = Depends(get_sma_service), user_id: int = None):
    return service.get_statistics(user_id)

@router.get("/{id}", response_model=None)
def get_movie(id: int, service: SMAService = Depends(get_sma_service)):
    movie = service.get_movie_by_id(id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie
