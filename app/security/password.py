from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'])


def hash_password(plained_password: str) -> str:
    return pwd_context.hash(secret=plained_password)


def verify_password(plained_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(secret=plained_password, hash=hashed_password)
