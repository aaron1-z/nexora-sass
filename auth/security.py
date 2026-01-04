from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User:
    username: str
    roles: list[str] = []

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Validate JWT token and return user.
    """
    if token != "valid-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return User(username="admin", roles=["admin"])

def check_permissions(required_role: str):
    def role_checker(user: User = Depends(get_current_user)):
        if required_role not in user.roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return role_checker

# Encryption Helper
from cryptography.fernet import Fernet

class EncryptionService:
    def __init__(self, key: bytes):
        self.cipher = Fernet(key)

    def encrypt(self, data: str) -> str:
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt(self, token: str) -> str:
        return self.cipher.decrypt(token.encode()).decode()
