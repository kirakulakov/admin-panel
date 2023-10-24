from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify(*, password: str, user_hashed_password: str) -> bool:
    if not pwd_context.verify(password, user_hashed_password):
        return False

    return True
