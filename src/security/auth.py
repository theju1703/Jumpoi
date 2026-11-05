"""
Enterprise Authentication & Role-Based Access Control (RBAC) Module
Implements secure password hashing with bcrypt, JWT bearer token signing and validation,
and permission enforcement across supermarket roles: ADMIN, STORE_MANAGER, CASHIER, INVENTORY_STAFF.
"""

import os
import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
import bcrypt
import jwt
from fastapi import HTTPException, Security, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field

# Security Configuration
SECRET_KEY = os.getenv("ERP_SECRET_KEY", "jompoi-enterprise-supermarket-secret-key-2026-prod")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 12  # 12-hour session duration for retail shifts

security = HTTPBearer(auto_error=False)

# ---------------------------------------------------------------------------
# Password & Hashing Utilities
# ---------------------------------------------------------------------------

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False

# ---------------------------------------------------------------------------
# Roles & User Schemas
# ---------------------------------------------------------------------------

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    STORE_MANAGER = "STORE_MANAGER"
    CASHIER = "CASHIER"
    INVENTORY_STAFF = "INVENTORY_STAFF"

class UserRegister(BaseModel):
    username: str
    password: str = Field(..., min_length=6)
    full_name: str
    role: UserRole = UserRole.CASHIER

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    username: str
    full_name: str
    role: UserRole
    created_at: str

# In-memory user directory seeded with default roles for supermarket operations
_DEFAULT_USERS: Dict[str, Dict[str, Any]] = {
    "admin": {
        "username": "admin",
        "password_hash": hash_password("admin123"),
        "full_name": "Senior Enterprise Administrator",
        "role": UserRole.ADMIN.value,
        "created_at": "2026-01-01T00:00:00Z"
    },
    "manager": {
        "username": "manager",
        "password_hash": hash_password("manager123"),
        "full_name": "Store Branch General Manager",
        "role": UserRole.STORE_MANAGER.value,
        "created_at": "2026-01-01T00:00:00Z"
    },
    "cashier": {
        "username": "cashier",
        "password_hash": hash_password("cashier123"),
        "full_name": "POS Counter Cashier Staff",
        "role": UserRole.CASHIER.value,
        "created_at": "2026-01-01T00:00:00Z"
    },
    "inventory": {
        "username": "inventory",
        "password_hash": hash_password("inventory123"),
        "full_name": "Warehouse & Stock Floor Specialist",
        "role": UserRole.INVENTORY_STAFF.value,
        "created_at": "2026-01-01T00:00:00Z"
    }
}

# ---------------------------------------------------------------------------
# JWT Token Utilities
# ---------------------------------------------------------------------------

def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + (
        expires_delta or datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire, "iat": datetime.datetime.now(datetime.timezone.utc)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        return None

def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    try:
        from src.config.settings import MONGO_URI, MONGO_DB_NAME
        from pymongo import MongoClient
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=800)
        user = client[MONGO_DB_NAME]["users"].find_one({"username": username})
        if user:
            user["_id"] = str(user["_id"])
            return user
    except Exception:
        pass
    return _DEFAULT_USERS.get(username)

def save_user(user_doc: Dict[str, Any]) -> None:
    try:
        from src.config.settings import MONGO_URI, MONGO_DB_NAME
        from pymongo import MongoClient
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=800)
        client[MONGO_DB_NAME]["users"].replace_one({"username": user_doc["username"]}, user_doc, upsert=True)
    except Exception:
        pass
    _DEFAULT_USERS[user_doc["username"]] = user_doc

def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Security(security)) -> Dict[str, Any]:
    if not credentials:
        if os.environ.get("ERP_STRICT_AUTH", "false").lower() == "true":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication credentials were not provided",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # For ease of local dev fallback
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
