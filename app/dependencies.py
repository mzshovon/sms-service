import secrets
import time
from collections import defaultdict, deque
from threading import Lock

from fastapi import Header, HTTPException, status

from app.config import Settings, get_settings
from app.provider_client import ProviderClient, make_provider_client
from app.services.dlr import DlrService
from app.services.send_sms import SendSmsService

_rate_limit_lock = Lock()
_send_attempts: dict[str, deque[float]] = defaultdict(deque)


def get_provider_client() -> ProviderClient:
    return make_provider_client(get_settings())


def get_send_sms_service() -> SendSmsService:
    settings = get_settings()
    return SendSmsService(make_provider_client(settings), settings)


def get_dlr_service() -> DlrService:
    settings = get_settings()
    return DlrService(make_provider_client(settings), settings)


def verify_api_client(
    x_client_id: str | None = Header(None, alias="X-Client-Id"),
    x_client_password: str | None = Header(None, alias="X-Client-Password"),
) -> str:
    settings = get_settings()
    if not settings.api_auth_enabled:
        return "auth-disabled"

    if not settings.api_client_id or not settings.api_client_password:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API client credentials are not configured",
        )

    is_valid_client_id = (
        x_client_id is not None
        and secrets.compare_digest(x_client_id, settings.api_client_id)
    )
    is_valid_password = (
        x_client_password is not None
        and secrets.compare_digest(x_client_password, settings.api_client_password)
    )
    if not is_valid_client_id or not is_valid_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API client credentials",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    return settings.api_client_id


def enforce_send_rate_limit(client_id: str) -> None:
    settings = get_settings()
    max_requests = settings.sms_send_rate_limit_requests
    window_seconds = settings.sms_send_rate_limit_window_seconds
    if max_requests <= 0 or window_seconds <= 0:
        return

    now = time.monotonic()
    window_start = now - window_seconds

    with _rate_limit_lock:
        attempts = _send_attempts[client_id]
        while attempts and attempts[0] <= window_start:
            attempts.popleft()

        if len(attempts) >= max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="SMS send rate limit exceeded",
                headers={"Retry-After": str(window_seconds)},
            )

        attempts.append(now)
