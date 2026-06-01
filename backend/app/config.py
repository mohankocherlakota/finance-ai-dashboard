from functools import lru_cache
from typing import List

from dotenv import dotenv_values
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "finance-ai-dashboard"
    database_url: str = "sqlite:///./finance_ai.db"
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    plaid_client_id: str = ""
    plaid_secret: str = ""
    plaid_access_token: str = ""
    plaid_item_id: str = "env_plaid_item"
    plaid_env: str = "sandbox"
    plaid_products: str = "transactions"
    plaid_country_codes: str = "US"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origin_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def plaid_access_tokens(self) -> dict[str, str]:
        values = dotenv_values(".env")
        tokens: dict[str, str] = {}
        if self.plaid_access_token:
            tokens[self.plaid_item_id] = self.plaid_access_token
        for key, value in values.items():
            if key.upper().startswith("PLAID_ACCESS_TOKEN") and value:
                item_key = key.lower().replace("plaid_access_token", "env_plaid_item").replace("__", "_")
                tokens[item_key] = value
        return tokens


@lru_cache
def get_settings() -> Settings:
    return Settings()
