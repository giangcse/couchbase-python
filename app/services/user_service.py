import uuid
from couchbase.exceptions import DocumentExistsException, DocumentNotFoundException
from app.db.session import get_user_collection, cluster
from app.core.security import get_password_hash, verify_password
from app.schemas.user import UserCreate, UserInDB, User
from couchbase.options import QueryOptions
from couchbase.result import QueryResult
from app.core.config import settings


collection = get_user_collection() # Sử dụng get_user_collection()

async def create_user(user: UserCreate) -> UserInDB:
    user_id = f"{uuid.uuid4()}"
    hashed_password = get_password_hash(user.password)
    user_data = {**user.model_dump(exclude={"password"}), "hashed_password": hashed_password, "type": "user"}
    try:
        collection.insert(user_id, user_data)
        return UserInDB(id=user_id, **user_data)
    except DocumentExistsException:
        return None

async def authenticate_user(username: str, password: str):
    query = f"SELECT META(u).id, u.* FROM `{settings.COUCHBASE_BUCKET}`.userscope.users u WHERE u.type = 'user' AND u.username = '{username}'"
    result: QueryResult = cluster.query(query, QueryOptions(adhoc=False))
    user_data = next(result.rows(), None)

    if user_data:
        if verify_password(password, user_data["hashed_password"]):
            return User(id=user_data["id"], username=user_data["username"], email=user_data["email"])
        return None
    return None

async def get_user_by_username(username: str):
    query = f"SELECT META(u).id, u.* FROM `{settings.COUCHBASE_BUCKET}`.userscope.users u WHERE u.type = 'user' AND u.username = '{username}'"
    result: QueryResult = cluster.query(query, QueryOptions(adhoc=False))
    user_data = next(result.rows(), None)
    if user_data:
        return User(id=user_data["id"], username=user_data["username"], email=user_data["email"])
    return None