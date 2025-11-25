import os
import re
from typing import Optional

from fastapi import FastAPI, Header, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from postgrest.exceptions import APIError

from supabase import create_client

try:
    from dotenv import load_dotenv

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    dotenv_path = os.path.join(repo_root, ".env")
    load_dotenv(dotenv_path)
except Exception:
    try:
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        dotenv_path = os.path.join(repo_root, ".env")
        if not os.path.exists(dotenv_path):
            dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
        if os.path.exists(dotenv_path):
            with open(dotenv_path, "r", encoding="utf-8") as fh:
                for ln in fh:
                    ln = ln.strip()
                    if not ln or ln.startswith("#"):
                        continue
                    if "=" in ln:
                        k, v = ln.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip('"').strip("'")
                        if k and (k not in os.environ):
                            os.environ[k] = v
    except Exception:
        pass


SUPABASE_URL: str = os.environ.get("SUPABASE_URL") or os.environ.get("VITE_SUPABASE_URL")
SUPABASE_KEY: str = (
    os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    or os.environ.get("SUPABASE_KEY")
    or os.environ.get("VITE_SUPABASE_ANON_KEY")
)

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in environment")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RecordIn(BaseModel):
    user_id: str
    record_type: str
    amount: float
    category: str
    purpose: str
    status: Optional[str] = "active"


def _resp_to_tuple(resp):
    data = getattr(resp, "data", None)
    error = getattr(resp, "error", None)
    if data is None and isinstance(resp, dict):
        data = resp.get("data")
        error = resp.get("error")
    return data, error


def _get_bearer_token(authorization: Optional[str]) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    return parts[1]


def _get_user_by_token(token: str):
    try:
        resp_user = supabase.auth.get_user(token)
        if isinstance(resp_user, dict):
            user = resp_user.get("data") or resp_user.get("user")
            err = resp_user.get("error")
        else:
            user = getattr(resp_user, "data", None) or getattr(resp_user, "user", None)
            err = getattr(resp_user, "error", None)
        if err:
            raise HTTPException(status_code=401, detail=str(err))
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"failed to validate token: {e}")


def _extract_discord_id(user) -> Optional[str]:
    try:
        if isinstance(user, dict):
            identities = user.get("identities") or user.get("user_metadata", {}).get("identities")
        else:
            identities = getattr(user, "identities", None)
        if identities and isinstance(identities, (list, tuple)) and len(identities) > 0:
            first = identities[0]
            if isinstance(first, dict):
                return first.get("id")
            return getattr(first, "id", None)
    except Exception:
        return None
    return None


def _ensure_admin(discord_id: str) -> None:
    try:
        resp_admin = supabase.from_("admin_list").select("*").eq("discord_id", discord_id).limit(1).execute()
        admin_data, admin_err = _resp_to_tuple(resp_admin)
        if admin_err:
            raise HTTPException(status_code=500, detail=str(admin_err))
        if not (admin_data and len(admin_data) > 0):
            raise HTTPException(status_code=403, detail="admin access required")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"admin check failed: {e}")


def _fetch_records_sorted() -> list:
    resp = supabase.from_("financial_records").select("*").execute()
    data, error = _resp_to_tuple(resp)
    if error:
        raise HTTPException(status_code=500, detail=str(error))
    if not data:
        return []
    try:
        if isinstance(data, list):
            data = sorted(data, key=lambda r: r.get("created_at") or "", reverse=True)
    except Exception:
        pass
    return data or []

@app.get("/api/records")
def get_records(authorization: Optional[str] = Header(None, alias="Authorization")):
    token = _get_bearer_token(authorization)
    user = _get_user_by_token(token)
    discord_id = _extract_discord_id(user)
    if not discord_id:
        raise HTTPException(status_code=403, detail="could not determine discord id from token")
    _ensure_admin(discord_id)
    return _fetch_records_sorted()


@app.post("/api/records")
def create_record(record: RecordIn, authorization: Optional[str] = Header(None)):
    payload = record.dict()
    try:
        if payload.get("amount") is not None:
            payload["amount"] = int(payload["amount"])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"invalid amount: {e}")

    resp = supabase.from_("financial_records").insert([payload]).execute()
    data, error = _resp_to_tuple(resp)
    if error:
        raise HTTPException(status_code=500, detail=str(error))
    return {"success": True, "data": data}


@app.patch("/api/records/{transaction_id}")
def update_record(transaction_id: str, payload: dict, authorization: Optional[str] = Header(None)):
    status = payload.get("status") if isinstance(payload, dict) else None
    if not status:
        raise HTTPException(status_code=400, detail="status is required in body")
    resp = supabase.from_("financial_records").update({"status": status}).eq("transaction_id", transaction_id).execute()
    _, error = _resp_to_tuple(resp)
    if error:
        raise HTTPException(status_code=500, detail=str(error))
    return {"success": True}


@app.get("/api/is_member")
def check_whitelist(discord_id: str):
    if not discord_id:
        raise HTTPException(status_code=400, detail="discord_id is required")
    resp = supabase.from_("member_list").select("*").eq("discord_id", discord_id).limit(1).execute()
    data, error = _resp_to_tuple(resp)
    if error:
        raise HTTPException(status_code=500, detail=str(error))
    return {"is_member": bool(data and len(data) > 0)}


@app.get("/api/is_admin")
def check_admin(discord_id: str):
    if not re.fullmatch(r"\d+", discord_id):
        return JSONResponse(status_code=400, content={"detail": "invalid discord_id, must be numeric"})
    try:
        resp = supabase.from_("admin_list").select("*").eq("discord_id", int(discord_id)).limit(1).execute()
        data = resp.data or []
        is_admin = len(data) > 0
        return {"is_admin": is_admin}
    except APIError as e:
        return JSONResponse(status_code=400, content={"detail": str(e)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": "internal error"})


@app.get("/api/user")
def get_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = parts[1]
    try:
        resp = supabase.auth.get_user(token)
        user = None
        if isinstance(resp, dict):
            user = resp.get("data") or resp.get("user")
            err = resp.get("error")
        else:
            user = getattr(resp, "data", None) or getattr(resp, "user", None)
            err = getattr(resp, "error", None)
        if err:
            raise HTTPException(status_code=401, detail=str(err))
        return {"user": user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
