from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Bookstore API"
    API_V1_STR: str = "/api/v1"
    COUCHBASE_USER: str = "giangpt"
    COUCHBASE_PASSWORD: str = "123123"
    COUCHBASE_CONNECTION_STRING: str = "127.0.0.1" # Đảm bảo đã khai báo COUCHBASE_CONNECTION_STRING
    COUCHBASE_BUCKET: str = "bookstore"
    SECRET_KEY: str = "VHOANG1912"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()