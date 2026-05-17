import jwt
from fastapi import Request, HTTPException, status, Depends
from utils.security import SECRET_KEY, ALGORITHM, SESSION_EXPIRY_MINUTES, redis_client


def get_current_user(request: Request) -> dict:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    redis_key = f"session:{token}"
    session_data_str = redis_client.get(redis_key)
    if not session_data_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or invalid"
        )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("purpose") != "session":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token scope")

        # 3. Sliding Session Window: Reset the TTL on Redis for active usage activity
        redis_client.expire(redis_key, SESSION_EXPIRY_MINUTES * 60)

        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")


def require_role(allowed_roles: list[str]):
    """
    Enforces route guards with strict role separation.
    If a route allows ['user'], admins are blocked, and vice-versa.
    """

    def dependency(current_user: dict = Depends(get_current_user)):
        if current_user.get("role") not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: Insufficient permissions"
            )
        return current_user

    return dependency