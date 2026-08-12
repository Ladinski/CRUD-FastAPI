from fastapi import APIRouter, HTTPException, status

from app.auth.supabase_client import supabase
from app.schemas.auth_schema import AuthRequest


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    summary="Sign up",
    description="Creates a new user account using Supabase Auth."
)
async def signup(data: AuthRequest):
    if not data.email or not data.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required"
        )

    if not data.email.strip() or not data.password.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required"
        )

    try:
        response = supabase.auth.sign_up({
            "email": data.email,
            "password": data.password
        })

        return {
            "user": response.user.model_dump(mode="json")
            if response.user
            else None
        }

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="Log in",
    description="Authenticates a user and returns Supabase access and refresh tokens."
)
async def login(data: AuthRequest):
    if not data.email or not data.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required"
        )

    if not data.email.strip() or not data.password.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required"
        )

    try:
        response = supabase.auth.sign_in_with_password({
            "email": data.email,
            "password": data.password
        })

        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token
        }

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login credentials"
        )