import os
import logging
from typing import List, Dict, Any, Optional

import discord

from core import supabase

logger = logging.getLogger(__name__)


async def sync_roles_with_supabase(
    bot: discord.Client,
    guild_id: Optional[int] = None,
    admin_role_id: Optional[int] = None,
    member_role_id: Optional[int] = None,
    remove_absent: bool = True,
) -> Dict[str, int]:
    """
    指定ギルドの `admin` / `member` ロール保有者を取得して
    Supabase の `admin_list` / `member_list` を upsert し、不要なレコードを削除します。
    """
    # env を優先して値を決定
    if guild_id is None:
        guild_id = int(os.getenv("DISCORD_GUILD_ID"))
    if admin_role_id is None:
        admin_role_id = int(os.getenv("DISCORD_ROLE_ID_ADMIN"))
    if member_role_id is None:
        member_role_id = int(os.getenv("DISCORD_ROLE_ID_MEMBER"))

    # guild を取得
    guild = bot.get_guild(guild_id)
    if guild is None:
        try:
            guild = await bot.fetch_guild(guild_id)
        except Exception as e:
            logger.exception("failed to fetch guild %s", guild_id)
            raise

    # members を確実に取得する (fetch_members が利用可能ならそちらを利用)
    members: List[discord.Member] = []
    try:
        # fetch_members returns an async iterator in discord.py
        async for m in guild.fetch_members(limit=None):
            members.append(m)
    except Exception:
        # フェッチが失敗した場合、キャッシュを使う (制限あり)
        members = list(getattr(guild, "members", []) or [])

    def _row_from_member(m: discord.Member) -> Dict[str, Any]:
        return {
            "discord_id": int(m.id),
            "username": f"{m.name}#{m.discriminator}",
            "display_name": m.display_name,
        }

    admin_rows = [r for r in (_row_from_member(m) for m in members) if any(r for r in [] )]
    # 上の行はプレースホルダなので正しくフィルタし直す
    admin_rows = [
        _row_from_member(m) for m in members if any(getattr(role, "id", None) == admin_role_id for role in m.roles)
    ]
    member_rows = [
        _row_from_member(m) for m in members if any(getattr(role, "id", None) == member_role_id for role in m.roles)
    ]

    # upsert admin_list: only discord_id (simpler, avoids schema mismatch)
    try:
        if admin_rows:
            id_only_rows = [{"discord_id": r["discord_id"]} for r in admin_rows]
            try:
                supabase.from_("admin_list").upsert(id_only_rows, on_conflict="discord_id").execute()
            except Exception as e:
                logger.exception("failed to upsert admin_list (discord_id only): %s", e)
                raise

            if remove_absent:
                ids = ",".join(str(r["discord_id"]) for r in id_only_rows)
                supabase.from_("admin_list").delete().filter("discord_id", "not.in", f"({ids})").execute()
        else:
            if remove_absent:
                print("admin")
                supabase.from_("admin_list").delete().execute()
    except Exception:
        logger.exception("failed to upsert/delete admin_list")
        raise

    # upsert member_list: only discord_id (simpler, avoids schema mismatch)
    try:
        if member_rows:
            id_only_rows = [{"discord_id": r["discord_id"]} for r in member_rows]
            try:
                supabase.from_("member_list").upsert(id_only_rows, on_conflict="discord_id").execute()
            except Exception as e:
                logger.exception("failed to upsert member_list (discord_id only): %s", e)
                raise

            if remove_absent:
                print("mem")
                ids = ",".join(str(r["discord_id"]) for r in id_only_rows)
                supabase.from_("member_list").delete().filter("discord_id", "not.in", f"({ids})").execute()
        else:
            if remove_absent:
                supabase.from_("member_list").delete().execute()
    except Exception:
        logger.exception("failed to upsert/delete member_list")
        raise

    return {"admins_synced": len(admin_rows), "members_synced": len(member_rows)}
