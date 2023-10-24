from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Server(BaseModel):
    host: str = '127.0.0.1'
    port: int = 8080
    log_level: str = 'info'
    reload: bool = False
    proxy_headers: bool = False
    workers: int = 1


class Psql(BaseModel):
    user: str = 'postgres'
    password: str = 'root'
    host: str = 'localhost'
    port: int = 5432
    database: str = 'admin_panel'
    pool_size: int = 10


class Secrets(BaseModel):
    secret_key: str = 'secret_key'
    encrypt_algorithm: str = 'HS256'


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='admin_panel_',
        env_nested_delimiter='__',
    )

    server: Server
    psql: Psql
    secrets: Secrets


settings = Settings()
