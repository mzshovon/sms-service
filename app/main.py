from typing import Annotated

from fastapi import Depends, FastAPI, Query

from app.dependencies import get_dlr_service, get_send_sms_service
from app.models import ProviderResponse, SendSmsRequest
from app.services.dlr import DlrService
from app.services.send_sms import SendSmsService

app = FastAPI(title="SMS Service")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/sms/send", response_model=ProviderResponse)
async def send_sms(
    payload: SendSmsRequest,
    service: Annotated[SendSmsService, Depends(get_send_sms_service)],
) -> dict:
    return await service.send(payload)


@app.get("/sms/dlr", response_model=ProviderResponse)
async def get_dlr(
    service: Annotated[DlrService, Depends(get_dlr_service)],
    message_id: Annotated[str | None, Query(alias="messageId")] = None,
    mobile_number: Annotated[str | None, Query(alias="mobileNumber")] = None,
) -> dict:
    return await service.get(message_id=message_id, mobile_number=mobile_number)
