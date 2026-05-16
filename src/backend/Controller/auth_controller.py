from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Service.auth_service import AuthService
from database import get_db
from Repository.user_repository import UserRepository
from Domain.models.user import UserModel

router = APIRouter(prefix="/auth", tags=["auth"])

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    repo = UserRepository(db)
    return AuthService(repo)

@router.post("/login")
async def login(data: dict, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.login_user(data)

@router.post("/register")
async def register(data: dict, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.register_user(data)