from typing import Any
from urllib.parse import urljoin

import httpx
from fastapi import HTTPException, status

from app.config import Settings


class ProviderClient:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    async def request(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        url = urljoin(self._settings.sms_api_base_url.rstrip("/") + "/", path.lstrip("/"))

        try:
            async with httpx.AsyncClient(timeout=self._settings.sms_timeout_seconds) as client:
                response = await client.request(method, url, json=json, params=params)
                response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            detail = _read_response(exc.response)
            raise HTTPException(
                status_code=exc.response.status_code,
                detail={"message": "SMS provider request failed", "provider": detail},
            ) from exc
        except httpx.HTTPError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail={"message": "SMS provider is unavailable"},
            ) from exc

        return {
            "status_code": response.status_code,
            "data": _read_response(response),
        }


def make_provider_client(settings: Settings) -> ProviderClient:
    return ProviderClient(settings)


def _read_response(response: httpx.Response) -> Any:
    try:
        return response.json()
    except ValueError:
        return response.text
