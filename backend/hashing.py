from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_pswd, hashed_pswd):
    return pwd_context.verify(plain_pswd, hashed_pswd)


def hash_password(password):
    return pwd_context.hash(password)