import re
from datetime import datetime, timezone, timedelta
from typing import Optional

from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from core import get_bearer_token, get_user_by_token, extract_discord_id_from_user, supabase
from cruds.db import check_member

router = APIRouter()

# 投票期間 (JST: UTC+9)
JST = timezone(timedelta(hours=9))
VOTE_START = datetime(2025, 12, 18, 0, 0, 0, tzinfo=JST)
VOTE_END = datetime(2025, 12, 18, 19, 0, 0, tzinfo=JST)


def _resp_to_tuple(resp):
    data = getattr(resp, "data", None)
    error = getattr(resp, "error", None)
    if data is None and isinstance(resp, dict):
        data = resp.get("data")
        error = resp.get("error")
    return data, error


def is_voting_period() -> bool:
    """現在が投票期間内かどうかを判定"""
    now = datetime.now(JST)
    return VOTE_START <= now <= VOTE_END


def get_voting_period_status() -> dict:
    """投票期間のステータスを返す"""
    now = datetime.now(JST)
    if now < VOTE_START:
        return {"status": "before", "message": "投票期間前です", "start": VOTE_START.isoformat(), "end": VOTE_END.isoformat()}
    elif now > VOTE_END:
        return {"status": "after", "message": "投票期間は終了しました", "start": VOTE_START.isoformat(), "end": VOTE_END.isoformat()}
    else:
        return {"status": "open", "message": "投票受付中", "start": VOTE_START.isoformat(), "end": VOTE_END.isoformat()}


def get_vote_by_discord_id(discord_id: int) -> Optional[dict]:
    """discord_idで投票データを取得"""
    resp = supabase.from_("vote_data").select("*").eq("discord_id", discord_id).limit(1).execute()
    data, error = _resp_to_tuple(resp)
    if error:
        raise RuntimeError(str(error))
    if data and len(data) > 0:
        return data[0]
    return None


def insert_vote(discord_id: int, vote: bool) -> dict:
    """投票を登録"""
    payload = {"discord_id": discord_id, "vote": vote}
    resp = supabase.from_("vote_data").insert([payload]).execute()
    data, error = _resp_to_tuple(resp)
    if error:
        raise RuntimeError(str(error))
    return data


class VoteRequest(BaseModel):
    vote: bool  # True: 賛成, False: 反対


@router.get("/api/vote/status")
def get_vote_status(authorization: Optional[str] = Header(None)):
    """自分の投票状態と投票期間を確認"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    try:
        token = get_bearer_token(authorization)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    try:
        user = get_user_by_token(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    discord_id_str = extract_discord_id_from_user(user)
    if not discord_id_str:
        raise HTTPException(status_code=400, detail="Discord ID not found in user data")
    
    try:
        discord_id = int(discord_id_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Discord ID format")
    
    # メンバー権限チェック
    try:
        is_member = check_member(discord_id_str)
    except Exception:
        is_member = False
    
    # 投票期間ステータス
    period_status = get_voting_period_status()
    
    # 投票済みかチェック
    try:
        existing_vote = get_vote_by_discord_id(discord_id)
        has_voted = existing_vote is not None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    return {
        "is_member": is_member,
        "has_voted": has_voted,
        "period": period_status
    }


@router.post("/api/vote")
def submit_vote(vote_request: VoteRequest, authorization: Optional[str] = Header(None)):
    """投票を登録"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    try:
        token = get_bearer_token(authorization)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    try:
        user = get_user_by_token(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    discord_id_str = extract_discord_id_from_user(user)
    if not discord_id_str:
        raise HTTPException(status_code=400, detail="Discord ID not found in user data")
    
    try:
        discord_id = int(discord_id_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Discord ID format")
    
    # メンバー権限チェック
    try:
        is_member = check_member(discord_id_str)
    except Exception:
        is_member = False
    
    if not is_member:
        raise HTTPException(status_code=403, detail="メンバー権限がありません")
    
    # 投票期間チェック
    if not is_voting_period():
        period_status = get_voting_period_status()
        raise HTTPException(status_code=400, detail=period_status["message"])
    
    # 投票済みチェック
    try:
        existing_vote = get_vote_by_discord_id(discord_id)
        if existing_vote is not None:
            raise HTTPException(status_code=400, detail="既に投票済みです。投票の変更はできません。")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    # 投票登録
    try:
        insert_vote(discord_id, vote_request.vote)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"投票の登録に失敗しました: {str(e)}")
    
    return {"success": True, "message": "投票が完了しました"}
