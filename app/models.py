from typing import Any

from pydantic import BaseModel, Field


class SendSmsRequest(BaseModel):
    campaign_name: str = Field(..., min_length=1, alias="campaignName")
    transaction_type: str = Field("T", min_length=1, alias="transactionType")
    mobile_number: str = Field(..., min_length=1, alias="mobileNumber")
    message: str = Field(..., min_length=1)

    model_config = {"populate_by_name": True}


class ProviderResponse(BaseModel):
    status_code: int
    data: Any
