from pydantic_settings import BaseSettings

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass


class Settings(BaseSettings):
    database_url: str
    uvicorn_host: str = "0.0.0.0"
    uvicorn_port: int = 8000

    class Config:
        env_prefix = ""
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
