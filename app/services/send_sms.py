from app.config import Settings
from app.models import SendSmsRequest
from app.provider_client import ProviderClient


class SendSmsService:
    def __init__(self, client: ProviderClient, settings: Settings) -> None:
        self._client = client
        self._settings = settings

    async def send(self, payload: SendSmsRequest) -> dict:
        provider_payload = {
            "apiKey": self._settings.sms_api_key,
            "userName": self._settings.sms_sender_id,
            "campaignName": payload.campaign_name,
            "senderName": self._settings.sms_sender_name,
            "transactionType": payload.transaction_type,
            "mobileNumber": payload.mobile_number,
            "message": payload.message,
        }
        return await self._client.request(
            "POST",
            self._settings.sms_send_path,
            json=provider_payload,
        )
