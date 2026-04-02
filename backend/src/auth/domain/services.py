from datetime import datetime, timedelta
from uuid import UUID

from jose import JWTError, jwt
from passlib.context import CryptContext

from src.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordService:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)


class JWTService:
    @staticmethod
    def create_access_token(user_id: UUID, tenant_id: UUID, role: str) -> str:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        payload = {
            "sub": str(user_id),
            "tenant_id": str(tenant_id),
            "role": role,
            "exp": expire,
            "type": "access",
        }
        return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)

    @staticmethod
    def create_refresh_token(user_id: UUID, tenant_id: UUID) -> str:
        expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
        payload = {
            "sub": str(user_id),
            "tenant_id": str(tenant_id),
            "exp": expire,
            "type": "refresh",
        }
        return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            return jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
        except JWTError:
            raise ValueError("Token inválido ou expirado")
