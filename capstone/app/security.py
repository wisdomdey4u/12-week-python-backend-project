from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_access_token(
    user_id: UUID,
    secret_key: str,
    expires_in_minutes: int,
) -> str:
    expires_at = datetime.now(UTC) + timedelta(minutes=expires_in_minutes)
    return jwt.encode(
        {"sub": str(user_id), "exp": expires_at},
        secret_key,
        algorithm="HS256",
    )
