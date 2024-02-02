from fastapi.security import APIKeyHeader
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

apikey_scheme = APIKeyHeader(name='Authorization')


class Hasher:
    @staticmethod
    def verify_password(plain_password, hashed_password) -> CryptContext:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password) -> CryptContext:
        return pwd_context.hash(password)
