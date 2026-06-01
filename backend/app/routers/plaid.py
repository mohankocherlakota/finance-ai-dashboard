from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.models import Account, AppSetting, PlaidItem, Transaction
from app.plaid_client import create_link_token, exchange_public_token, sync_transactions
from app.schemas import ExchangePublicTokenRequest, LinkTokenResponse, MessageResponse


router = APIRouter()


@router.post("/create_link_token", response_model=LinkTokenResponse)
def create_token():
    return LinkTokenResponse(link_token=create_link_token())


@router.post("/exchange_public_token", response_model=MessageResponse)
def exchange_token(payload: ExchangePublicTokenRequest, db: Session = Depends(get_db)):
    result = exchange_public_token(payload.public_token)
    item = db.query(PlaidItem).filter(PlaidItem.item_id == result["item_id"]).first()
    if not item:
        # TODO: Encrypt Plaid access tokens at rest before production deployment.
        item = PlaidItem(item_id=result["item_id"], access_token=result["access_token"], cursor="")
        db.add(item)
    else:
        # TODO: Encrypt Plaid access tokens at rest before production deployment.
        item.access_token = result["access_token"]
    db.merge(AppSetting(key="plaid_connected", value="true"))
    db.commit()
    return MessageResponse(message="Plaid public token exchanged")


@router.post("/sync_transactions", response_model=MessageResponse)
def sync(db: Session = Depends(get_db)):
    settings = get_settings()
    default_account = db.query(Account).filter(Account.plaid_account_id == "plaid_default").first()
    if not default_account:
        default_account = Account(
            plaid_account_id="plaid_default",
            name="Plaid Account",
            type="depository",
            subtype="checking",
            mask="0000",
        )
        db.add(default_account)
        db.flush()

    configured_tokens = settings.plaid_access_tokens
    items = db.query(PlaidItem).all()
    if configured_tokens:
        for item_id, access_token in configured_tokens.items():
            item = db.query(PlaidItem).filter(PlaidItem.item_id == item_id).first()
            if not item:
                # TODO: Encrypt Plaid access tokens at rest before production deployment.
                item = PlaidItem(item_id=item_id, access_token=access_token, cursor="")
                db.add(item)
                db.flush()
                items.append(item)
            else:
                # TODO: Encrypt Plaid access tokens at rest before production deployment.
                item.access_token = access_token
    if not items:
        raise HTTPException(status_code=400, detail="No Plaid item connected")

    total_added = 0
    for item in items:
        result = sync_transactions(item.access_token, item.cursor or None)
        item.cursor = result["next_cursor"]
        for row in result["added"]:
            tx_id = row.get("transaction_id")
            if db.query(Transaction).filter(Transaction.plaid_transaction_id == tx_id).first():
                continue
            category = row.get("personal_finance_category") or {}
            db.add(
                Transaction(
                    plaid_transaction_id=tx_id,
                    date=row.get("date"),
                    name=row.get("name") or "",
                    merchant_name=row.get("merchant_name") or row.get("name") or "",
                    amount=float(row.get("amount") or 0),
                    category_primary=category.get("primary") or "Other",
                    category_detailed=category.get("detailed") or "",
                    account_id=default_account.id,
                    pending=bool(row.get("pending")),
                )
            )
            total_added += 1
    db.commit()
    return MessageResponse(message=f"Synced {total_added} new transactions")
