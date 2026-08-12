from fastapi import APIRouter, Header, HTTPException, status
from app.auth.supabase_client import supabase

router = APIRouter(tags=["Protected"])


@router.get(
    "/public/info",
    summary="Public information",
    description="Returns public information without authentication."
)
async def public_info():
    return {
        "message": "Welcome stranger! This info is public."
    }


@router.get(
    "/protected/profile",
    summary="Protected profile",
    description="Returns the authenticated user's profile."
)
async def protected_profile(
    authorization: str | None = Header(default=None)
):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token required"
        )

    parts = authorization.split(" ", 1)

    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token required"
        )

    token = parts[1].strip()

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token required"
        )

    try:
        response = supabase.auth.get_user(token)
        user = response.user

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )

        return {
            "id": user.id,
            "email": user.email,
            "created_at": user.created_at
        }

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )