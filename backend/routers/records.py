from typing import Optional

from fastapi import APIRouter, Header, HTTPException

from core import get_bearer_token, get_user_by_token, extract_discord_id_from_user
from cruds.db import fetch_records_sorted, insert_record, update_record_status, ensure_admin
from pydantic import BaseModel


router = APIRouter()


class RecordIn(BaseModel):
    user_id: str
    record_type: str
    amount: float
    category: str
    purpose: str
    status: Optional[str] = "active"
    evidence_file_link: Optional[str] = None


@router.get("/api/records")
def get_records(authorization: Optional[str] = Header(None, alias="Authorization")):
    return fetch_records_sorted()


@router.post("/api/records")
def create_record(record: RecordIn, authorization: Optional[str] = Header(None)):
    payload = record.dict()
    try:
        if payload.get("amount") is not None:
            payload["amount"] = int(payload["amount"])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"invalid amount: {e}")
    try:
        data = insert_record(payload)
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/api/records/{transaction_id}")
def update_record(transaction_id: str, payload: dict, authorization: Optional[str] = Header(None)):
    try:
        token = get_bearer_token(authorization)
    except ValueError:
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")
    try:
        user = get_user_by_token(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

    discord_id = extract_discord_id_from_user(user)
    if not discord_id:
        raise HTTPException(status_code=403, detail="could not determine discord id from token")
    if not ensure_admin(discord_id):
        raise HTTPException(status_code=403, detail="admin access required")

    status = payload.get("status") if isinstance(payload, dict) else None
    if not status:
        raise HTTPException(status_code=400, detail="status is required in body")
    try:
        update_record_status(transaction_id, status)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
