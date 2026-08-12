from fastapi import APIRouter, Header, HTTPException, status


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
    description="Requires a Bearer access token in the Authorization header."
)
async def protected_profile(
    authorization: str | None = Header(default=None)
):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token required"
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token required"
        )

    token = authorization.removeprefix("Bearer ").strip()

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token required"
        )

    return {
        "message": "Token received",
        "token": token
    }