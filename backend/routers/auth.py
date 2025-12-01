import re
from typing import Optional

from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import JSONResponse

from core import get_bearer_token, get_user_by_token
from cruds.db import check_member, check_admin_by_id


router = APIRouter()


@router.get("/api/is_member")
def check_whitelist(discord_id: str):
    if not discord_id:
        raise HTTPException(status_code=400, detail="discord_id is required")
    try:
        is_member = check_member(discord_id)
        return {"is_member": is_member}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/is_admin")
def check_admin(discord_id: str):
    if not re.fullmatch(r"\d+", discord_id):
        return JSONResponse(status_code=400, content={"detail": "invalid discord_id, must be numeric"})
    try:
        is_admin = check_admin_by_id(int(discord_id))
        return {"is_admin": is_admin}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": "internal error"})


@router.get("/api/user")
def get_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    try:
        token = get_bearer_token(authorization)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    try:
        user = get_user_by_token(token)
        return {"user": user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
