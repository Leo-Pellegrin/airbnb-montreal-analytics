# backend/app/core/auth.py

from datetime import datetime, timedelta, timezone
from typing import Any, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.core.config import settings

# Sécurité HTTP Bearer (pour extraire le token)
security = HTTPBearer()


def create_access_token(sub: Union[str, Any]) -> str:
    """
    Génère un JWT avec un champ 'sub' (subject) et une date d'expiration.
    """
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode = {"exp": expire, "sub": str(sub)}
    encoded_jwt = jwt.encode(
        to_encode, settings.JWTSECRET, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


async def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """
    Dépendance à passer sur les routes protégées.
    Retourne le 'sub' du token (ex. user_id) ou lève 401 si invalide.
    """
    token = creds.credentials
    try:
        payload = jwt.decode(
            token, settings.JWTSECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
