from pydantic import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    pinecone_api_key: str
    serp_api_key: str
    youtube_api_key: str
    debug: bool
    api_version: str

    class Config:
        env_file = ".env"