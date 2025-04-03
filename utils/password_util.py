from passlib.hash import pbkdf2_sha256


def hash(password:str):
    return pbkdf2_sha256.hash(password)

def verify(password:str, hashed_password: str):
    return pbkdf2_sha256.verify(password, hashed_password)
