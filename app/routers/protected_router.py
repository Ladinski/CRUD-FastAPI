from app.auth.supabase_client import supabase
from fastapi import APIRouter, Depends, HTTPException, Response, status
from app.auth.dependencies import get_current_user


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
    auth=Depends(get_current_user)
):
    user = auth["user"]

    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at
    }


@router.get(
    "/protected/dashboard",
    summary="Protected dashboard",
    description="Returns protected dashboard information."
)
async def protected_dashboard(
    auth=Depends(get_current_user)
):
    user = auth["user"]

    return {
        "message": "Welcome to the protected dashboard",
        "user_id": user.id
    }

@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Log out",
    description="Logs out the authenticated user."
)
async def logout(
    auth=Depends(get_current_user)
):
    try:
        supabase.auth.sign_out()

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Logout failed"
        )