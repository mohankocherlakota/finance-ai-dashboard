from fastapi import HTTPException
from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.api_client import ApiClient

from app.config import get_settings


def get_plaid_client() -> plaid_api.PlaidApi:
    settings = get_settings()
    if not settings.plaid_client_id or not settings.plaid_secret:
        raise HTTPException(status_code=400, detail="Plaid credentials are not configured")
    host = plaid_host(settings.plaid_env)
    configuration = Configuration(
        host=host,
        api_key={"clientId": settings.plaid_client_id, "secret": settings.plaid_secret},
    )
    return plaid_api.PlaidApi(ApiClient(configuration))


def plaid_host(env: str) -> str:
    hosts = {
        "sandbox": "https://sandbox.plaid.com",
        "development": "https://development.plaid.com",
        "production": "https://production.plaid.com",
    }
    normalized = env.lower().strip()
    if normalized not in hosts:
        raise HTTPException(status_code=400, detail="PLAID_ENV must be sandbox, development, or production")
    return hosts[normalized]


def create_link_token() -> str:
    settings = get_settings()
    client = get_plaid_client()
    request = LinkTokenCreateRequest(
        products=[Products("transactions")],
        client_name=settings.app_name,
        country_codes=[CountryCode("US")],
        language="en",
        user=LinkTokenCreateRequestUser(client_user_id="local-demo-user"),
    )
    response = client.link_token_create(request)
    return response["link_token"]


def exchange_public_token(public_token: str) -> dict:
    client = get_plaid_client()
    response = client.item_public_token_exchange(ItemPublicTokenExchangeRequest(public_token=public_token))
    return {"access_token": response["access_token"], "item_id": response["item_id"]}


def sync_transactions(access_token: str, cursor: str | None = None) -> dict:
    client = get_plaid_client()
    has_more = True
    added = []
    modified = []
    removed = []
    next_cursor = cursor
    while has_more:
        request_args = {"access_token": access_token}
        if next_cursor:
            request_args["cursor"] = next_cursor
        response = client.transactions_sync(TransactionsSyncRequest(**request_args))
        added.extend(response["added"])
        modified.extend(response["modified"])
        removed.extend(response["removed"])
        has_more = response["has_more"]
        next_cursor = response["next_cursor"]
    return {"added": added, "modified": modified, "removed": removed, "next_cursor": next_cursor}
