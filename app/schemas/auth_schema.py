from pydantic import BaseModel


class AuthRequest(BaseModel):
    email: str | None = None
    password: str | None = None