from app.config import Settings, get_settings
from app.provider_client import ProviderClient, make_provider_client
from app.services.dlr import DlrService
from app.services.send_sms import SendSmsService


def get_provider_client() -> ProviderClient:
    return make_provider_client(get_settings())


def get_send_sms_service() -> SendSmsService:
    settings = get_settings()
    return SendSmsService(make_provider_client(settings), settings)


def get_dlr_service() -> DlrService:
    settings = get_settings()
    return DlrService(make_provider_client(settings), settings)
