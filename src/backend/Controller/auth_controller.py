from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from Domain.models.user import UserModel

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(data: dict, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter_by(
        username= data.get("username"),
        password = data.get("password")
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "id": user.id,
        "username": user.username,
        "role": user.role
    }

@router.post("/register")
async def register(data: dict, db: Session = Depends(get_db)):
    if db.query(UserModel).filter_by(username=data.get("username")).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    new_user = UserModel(
        username=data.get("username"),
        password=data.get("password"),
        role="user"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}