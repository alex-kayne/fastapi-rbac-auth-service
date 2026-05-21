from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str
    app_env: str
    debug: bool
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str
    access_token_expire_minutes: int
    password_hash_scheme: str

settings = Settings()
