import asyncio
from typing import Optional

from fastapi import APIRouter, HTTPException, Header

from cruds.discord_sync import sync_roles_with_supabase


def get_router(bot) -> APIRouter:
    router = APIRouter()

    @router.post("/admin/sync-admins")
    async def sync_admins(authorization: Optional[str] = Header(None, alias="Authorization")):
        # Optionally you could validate authorization here
        if bot is None:
            raise HTTPException(status_code=500, detail="discord bot not initialized")
        try:
            result = await sync_roles_with_supabase(bot, remove_absent=True)
            return {"success": True, "result": result}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/admin/sync-members")
    async def sync_members(authorization: Optional[str] = Header(None, alias="Authorization")):
        if bot is None:
            raise HTTPException(status_code=500, detail="discord bot not initialized")
        try:
            result = await sync_roles_with_supabase(bot, remove_absent=True)
            return {"success": True, "result": result}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return router
