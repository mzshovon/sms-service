from typing import Any

from app.config import Settings
from app.provider_client import ProviderClient


class DlrService:
    def __init__(self, client: ProviderClient, settings: Settings) -> None:
        self._client = client
        self._settings = settings

    async def get(self, message_id: str | None = None, mobile_number: str | None = None) -> dict:
        params: dict[str, Any] = {
            "apiKey": self._settings.sms_api_key,
            "userName": self._settings.sms_sender_id,
        }
        if message_id:
            params["messageId"] = message_id
        if mobile_number:
            params["mobileNumber"] = mobile_number

        return await self._client.request(
            "GET",
            self._settings.sms_dlr_path,
            params=params,
        )
