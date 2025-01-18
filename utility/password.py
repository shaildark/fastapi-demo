import bcrypt

def get_hashed_password(password) -> str:
    pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return pw.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))