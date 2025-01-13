from couchbase.collection import CBCollection
from couchbase.exceptions import DocumentExistsException, DocumentNotFoundException

from app.core.security import get_password_hash, verify_password
from app.db.session import get_db_collection
from app.schemas.user import UserCreate, UserInDB, User

def get_users_collection():
    return get_db_collection()

async def create_user(user: UserCreate) -> UserInDB:
    collection: CBCollection = get_users_collection()
    user_id = f"user::{user.username}"
    hashed_password = get_password_hash(user.password)
    user_data = {**user.dict(exclude={"password"}), "hashed_password": hashed_password, "type": "user"}
    try:
        collection.insert(user_id, user_data)
        return UserInDB(id=user_id, **user_data)
    except DocumentExistsException:
        return None

async def authenticate_user(username: str, password: str):
    collection: CBCollection = get_users_collection()
    user_id = f"user::{username}"
    try:
        result = collection.get(user_id)
        user_data = result.content_as[dict]
        if verify_password(password, user_data["hashed_password"]):
            return User(id=user_id, **user_data)
        return None
    except DocumentNotFoundException:
        return None

async def get_user_by_username(username: str):
    collection: CBCollection = get_users_collection()
    user_id = f"user::{username}"
    try:
        result = collection.get(user_id)
        user_data = result.content_as[dict]
        return User(id=user_id, **user_data)
    except DocumentNotFoundException:
        return None