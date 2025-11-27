from typing import Optional, List

from ..core import supabase


def _resp_to_tuple(resp):
    data = getattr(resp, "data", None)
    error = getattr(resp, "error", None)
    if data is None and isinstance(resp, dict):
        data = resp.get("data")
        error = resp.get("error")
    return data, error


def fetch_records_sorted() -> List[dict]:
    resp = supabase.from_("financial_records").select("*").execute()
    data, error = _resp_to_tuple(resp)
    if error:
        raise RuntimeError(str(error))
    if not data:
        return []
    try:
        if isinstance(data, list):
            data = sorted(data, key=lambda r: r.get("created_at") or "", reverse=True)
    except Exception:
        pass
    return data or []


def ensure_admin(discord_id: str) -> bool:
    resp = supabase.from_("admin_list").select("*").eq("discord_id", discord_id).limit(1).execute()
    data, error = _resp_to_tuple(resp)
    if error:
        raise RuntimeError(str(error))
    return bool(data and len(data) > 0)


def insert_record(payload: dict):
    resp = supabase.from_("financial_records").insert([payload]).execute()
    data, error = _resp_to_tuple(resp)
    if error:
        raise RuntimeError(str(error))
    return data


def update_record_status(transaction_id: str, status: str):
    resp = (
        supabase.from_("financial_records").update({"status": status}).eq("transaction_id", transaction_id).execute()
    )
    _, error = _resp_to_tuple(resp)
    if error:
        raise RuntimeError(str(error))
    return True


def check_member(discord_id: str) -> bool:
    resp = supabase.from_("member_list").select("*").eq("discord_id", discord_id).limit(1).execute()
    data, error = _resp_to_tuple(resp)
    if error:
        raise RuntimeError(str(error))
    return bool(data and len(data) > 0)


def check_admin_by_id(discord_id: int) -> bool:
    resp = supabase.from_("admin_list").select("*").eq("discord_id", discord_id).limit(1).execute()
    data, error = _resp_to_tuple(resp)
    if error:
        raise RuntimeError(str(error))
    return bool(data and len(data) > 0)
