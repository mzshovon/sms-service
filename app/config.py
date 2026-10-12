from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = Field("local", alias="APP_ENV")
    api_auth_enabled: bool = Field(True, alias="API_AUTH_ENABLED")
    api_client_id: str | None = Field(None, alias="API_CLIENT_ID")
    api_client_password: str | None = Field(None, alias="API_CLIENT_PASSWORD")
    sms_send_rate_limit_requests: int = Field(30, alias="SMS_SEND_RATE_LIMIT_REQUESTS")
    sms_send_rate_limit_window_seconds: int = Field(60, alias="SMS_SEND_RATE_LIMIT_WINDOW_SECONDS")
    sms_api_base_url: str = Field(..., alias="SMS_API_BASE_URL")
    sms_send_path: str = Field("/api/sms/send", alias="SMS_SEND_PATH")
    sms_dlr_path: str = Field("/api/sms/dlr", alias="SMS_DLR_PATH")
    sms_api_key: str = Field(..., alias="SMS_API_KEY")
    sms_sender_id: str = Field(..., alias="SMS_SENDER_ID")
    sms_sender_name: str = Field(..., alias="SMS_SENDER_NAME")
    sms_timeout_seconds: float = Field(10.0, alias="SMS_TIMEOUT_SECONDS")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()
