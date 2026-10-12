"""
CinePulse Supabase JWT Authentication Validator
Extracts and verifies Bearer JWT tokens, deriving the user context directly from the token.
"""
from typing import Optional
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from ..config import settings

security = HTTPBearer(auto_error=False)

class AuthenticatedUser(BaseModel):
    user_id: str
    email: Optional[str] = None
    role: Optional[str] = None

def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Security(security)) -> AuthenticatedUser:
    """
    Validates Supabase JWT from Authorization: Bearer <token>.
    Derives user_id from the 'sub' claim.
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials were not provided in Authorization header.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    # If Supabase JWT Secret is configured, verify HMAC signature
    if settings.SUPABASE_JWT_SECRET:
        try:
            payload = jwt.decode(
                token,
                settings.SUPABASE_JWT_SECRET,
                algorithms=["HS256"],
                options={"verify_aud": False}
            )
            user_id: str = payload.get("sub")
            if not user_id:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing subject claim.")
            email: Optional[str] = payload.get("email")
            role: Optional[str] = payload.get("role")
            return AuthenticatedUser(user_id=user_id, email=email, role=role)
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid or expired JWT authentication token: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )
    else:
        # Development / Sandbox mode: decode without secret verification if secret not yet set up
        try:
            unverified_claims = jwt.get_unverified_claims(token)
            user_id = unverified_claims.get("sub", "dev-user-001")
            email = unverified_claims.get("email", "dev@cinepulse.example.com")
            return AuthenticatedUser(user_id=user_id, email=email, role="authenticated")
        except Exception:
            # Fallback for simple dev mock tokens
            if token.startswith("mock_"):
                return AuthenticatedUser(user_id=token, email=f"{token}@cinepulse.test", role="authenticated")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Malformed JWT token structure.")

def get_optional_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Security(security)) -> Optional[AuthenticatedUser]:
    """Returns the authenticated user if credentials exist, otherwise None without raising 401."""
    if not credentials:
        return None
    try:
        return get_current_user(credentials)
    except HTTPException:
        return None
