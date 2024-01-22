from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

apikey_scheme = APIKeyHeader(name='Authorization')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


class Hasher:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)
