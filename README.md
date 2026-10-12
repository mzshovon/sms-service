# sms-service

Simple FastAPI wrapper for sending SMS messages and fetching delivery reports.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Update `.env` with the SMS provider base URL, endpoint paths, API key, and sender ID.

Set `APP_ENV=production` in deployed environments. Production disables `/docs`,
`/redoc`, and `/openapi.json`.

## Run

```bash
uvicorn app.main:app --reload
```

## Docker

Build the image:

```bash
docker build -t sms-service .
```

Run it with environment variables from `.env`; the app listens on `PORT`:

```bash
docker run --env-file .env -e PORT=8000 -p 8000:8000 sms-service
```

Or use Docker Compose:

```bash
docker compose up --build
```

## APIs

SMS endpoints require client credentials:

```bash
X-Client-Id: <API_CLIENT_ID>
X-Client-Password: <API_CLIENT_PASSWORD>
```

`/sms/send` is rate-limited by client id using `SMS_SEND_RATE_LIMIT_REQUESTS`
per `SMS_SEND_RATE_LIMIT_WINDOW_SECONDS`.

### Send SMS

`POST /sms/send`

```json
{
  "campaignName": "Product launch",
  "transactionType": "T",
  "mobileNumber": "8801939504445",
  "message": "hello there"
}
```

The service injects `apiKey` from `SMS_API_KEY`, plus `userName` and `senderName` from `SMS_SENDER_ID` before calling the provider.

### Get DLR

`GET /sms/dlr?messageId=<provider-message-id>`

or

`GET /sms/dlr?mobileNumber=8801939504445`

The service injects the same provider credentials as query parameters.
