from fastapi import HTTPException, status
from Repository.user_repository import UserRepository
from Domain.models.user import UserModel
from utils.security import hash_password, verify_password, create_access_token

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(self, data : dict) -> dict:
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise HTTPException(status_code=400, detail="Username and password are required")

        if self.user_repo.get_by_username(username):
            raise HTTPException(status_code=400, detail="Username already taken")

        hashed_password = hash_password(password)
        new_user = UserModel(
            username=username,
            password=hashed_password,
            role="user",
            image = "null",
        )

        self.user_repo.create(new_user)
        return {"message": "User created successfully"}

    async def login_user(self, data : dict) -> dict:
        username = data.get("username")
        password = data.get("password")

        user = self.user_repo.get_by_username(username)
        if not user or not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        token_payload = {
            "id": user.id,
            "username": user.username,
            "role": user.role
        }

        token = create_access_token(token_payload)

        return {
            "access_token": token,
            "token_type": "bearer",
            "id" : user.id,
            "role": user.role,
            "username": user.username,
            "image": user.image,
        }