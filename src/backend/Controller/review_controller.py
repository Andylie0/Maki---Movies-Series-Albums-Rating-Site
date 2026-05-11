from fastapi import APIRouter, Depends, HTTPException, Query
from Repository.log_repository import LogRepository
from Repository.review_repository import ReviewRepository
from Repository.sma_repository import SMARepository
from Service.log_service import LogService
from Service.review_service import ReviewService
from database import get_db
from sqlalchemy.orm import Session
from Service.websocket_manager import ws_manager

router = APIRouter(prefix="/reviews", tags=["Reviews"])

def get_review_service(db : Session = Depends(get_db)):
    log_repo = LogRepository(db)
    log_service = LogService(log_repo)

    return ReviewService(
        review_repo = ReviewRepository(db),
        sma_repo = SMARepository(db),
        log_service = log_service,
        ws_manager = ws_manager
    )

@router.get("/")
def get_reviews(
    page: int = Query(1, ge=1),
    size: int = Query(7, ge=1),
    user_id: int = Query(None),
    service: ReviewService = Depends(get_review_service)
):
    items, total = service.get_paginated_reviews(page, user_id, size)
    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size
    }

@router.post("/", response_model=None)
async def create_review(data: dict, user_id : int = Query(...) ,service: ReviewService = Depends(get_review_service)):
    return await service.add_review(data, user_id=user_id)

@router.put("/{review_id}", response_model=None)
async def update_review(review_id: int, data: dict, user_id : int = Query(...), service: ReviewService = Depends(get_review_service)):
    result = await service.update_review(review_id, data, user_id=user_id)
    if not result:
        raise HTTPException(status_code=404, detail="Review not found")
    return result

@router.delete("/{review_id}")
async def delete_review(review_id: int, user_id : int = Query(...), service: ReviewService = Depends(get_review_service)):
    success = await service.delete_review(review_id, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Review not found")
    return {"message": "Deleted successfully"}