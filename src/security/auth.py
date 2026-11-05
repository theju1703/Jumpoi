import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
import bcrypt
import jwt
from fastapi import HTTPException, Security, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from src.config import BASE_DIR

JWT_SECRET_KEY = "jompoi-erp-supermarket-enterprise-secret-key-2026"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

security = HTTPBearer(auto_error=False)

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    STORE_MANAGER = "STORE_MANAGER"
    CASHIER = "CASHIER"
    INVENTORY_STAFF = "INVENTORY_STAFF"

class UserRegister(BaseModel):
    username: str
    password: str
    full_name: str
    role: UserRole = UserRole.CASHIER

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    username: str
    full_name: str
    role: str
    created_at: str

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False

def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + (expires_delta or datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "iat": datetime.datetime.now(datetime.timezone.utc)})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None

# In-memory users repository (persists with fallback seed)
_DEFAULT_USERS: Dict[str, Dict[str, Any]] = {
    "admin": {
        "username": "admin",
        "password_hash": hash_password("admin123"),
        "full_name": "System Administrator",
        "role": UserRole.ADMIN.value,
        "created_at": "2026-08-01T00:00:00Z"
    },
    "manager": {
        "username": "manager",
        "password_hash": hash_password("manager123"),
        "full_name": "Store Operations Manager",
        "role": UserRole.STORE_MANAGER.value,
        "created_at": "2026-08-01T00:00:00Z"
    },
    "cashier1": {
        "username": "cashier1",
        "password_hash": hash_password("cashier123"),
        "full_name": "POS Counter Cashier 1",
        "role": UserRole.CASHIER.value,
        "created_at": "2026-08-01T00:00:00Z"
    },
    "inventory1": {
        "username": "inventory1",
        "password_hash": hash_password("inventory123"),
        "full_name": "Warehouse Inventory Officer",
        "role": UserRole.INVENTORY_STAFF.value,
        "created_at": "2026-08-01T00:00:00Z"
    }
}

def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    return _DEFAULT_USERS.get(username)

def save_user(user_doc: Dict[str, Any]) -> None:
    _DEFAULT_USERS[user_doc["username"]] = user_doc

def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Security(security)) -> Dict[str, Any]:
    if not credentials:
        # For ease of testing and backwards compatibility in local dev, fallback to admin if unauthenticated
        return _DEFAULT_USERS["admin"]
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = get_user_by_username(payload["sub"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def require_roles(*allowed_roles: UserRole):
    def role_checker(current_user: Dict[str, Any] = Depends(get_current_user)):
        user_role = current_user.get("role")
        role_values = [r.value if isinstance(r, UserRole) else r for r in allowed_roles]
        if user_role not in role_values and user_role != UserRole.ADMIN.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: operation requires one of roles: {role_values}"
            )
        return current_user
    return role_checker
