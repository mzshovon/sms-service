from typing import Annotated

from fastapi import Depends, FastAPI, Query

from app.config import get_settings
from app.dependencies import (
    enforce_send_rate_limit,
    get_dlr_service,
    get_send_sms_service,
    verify_api_client,
)
from app.models import ProviderResponse, SendSmsRequest
from app.services.dlr import DlrService
from app.services.send_sms import SendSmsService

settings = get_settings()
app = FastAPI(
    title="SMS Service",
    docs_url=None if settings.is_production else "/docs",
    redoc_url=None if settings.is_production else "/redoc",
    openapi_url=None if settings.is_production else "/openapi.json",
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/sms/send", response_model=ProviderResponse)
async def send_sms(
    payload: SendSmsRequest,
    service: Annotated[SendSmsService, Depends(get_send_sms_service)],
    client_id: Annotated[str, Depends(verify_api_client)],
) -> dict:
    enforce_send_rate_limit(client_id)
    return await service.send(payload)


@app.get("/sms/dlr", response_model=ProviderResponse)
async def get_dlr(
    service: Annotated[DlrService, Depends(get_dlr_service)],
    _: Annotated[str, Depends(verify_api_client)],
    message_id: Annotated[str | None, Query(alias="messageId")] = None,
    mobile_number: Annotated[str | None, Query(alias="mobileNumber")] = None,
) -> dict:
    return await service.get(message_id=message_id, mobile_number=mobile_number)
