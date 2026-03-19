"""配置管理模块"""

from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    llm_base_url: str = Field(default="https://api.deepseek.com", validation_alias="LLM_BASE_URL")
    llm_model_id: str = Field(default="deepseek-chat", validation_alias="LLM_MODEL_ID")
    llm_api_key: str = Field(default="", validation_alias="LLM_API_KEY")
    llm_fallback_base_url: Optional[str] = Field(default=None, validation_alias="LLM_BASE_URL_FALLBACK")
    llm_fallback_model_id: Optional[str] = Field(default=None, validation_alias="LLM_MODEL_ID_FALLBACK")

    collection_timeout: int = Field(default=30, validation_alias="COLLECTION_TIMEOUT")
    collection_max_retries: int = Field(default=3, validation_alias="COLLECTION_MAX_RETRIES")
    collection_max_concurrency: int = Field(default=10)

    chunk_max_tokens: int = Field(default=2000, validation_alias="CHUNK_MAX_TOKENS")
    chunk_overlap_tokens: int = Field(default=200)

    export_output_dir: Path = Field(default=Path("./output"))
    export_default_format: str = Field(default="json")

    debug: bool = Field(default=False)


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
