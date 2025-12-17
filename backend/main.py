import re
from typing import Optional

import os
import asyncio
import logging

import discord

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from routers import records as records_router
from routers import auth as auth_router
from routers import admin_sync as admin_sync_router
from routers import vote as vote_router

logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.members = True
discord_client: discord.Client = discord.Client(intents=intents)


@discord_client.event
async def on_ready():
    logger.info("discord client ready: %s", getattr(discord_client.user, "name", "?"))
    try:
        logger.info("roles synced on_ready")
    except Exception:
        logger.exception("failed to sync roles on ready")

_discord_task: asyncio.Task = None


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"detail": "backend running"}


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request, exc):
    print("RequestValidationError:", exc)
    return JSONResponse(status_code=422, content={"detail": exc.errors() if hasattr(exc, "errors") else str(exc)})


app.include_router(records_router.router)
app.include_router(auth_router.router)
app.include_router(admin_sync_router.get_router(discord_client))
app.include_router(vote_router.router)


@app.on_event("startup")
async def _startup_discord_client():
    """FastAPI 起動時に Discord クライアントを非同期で開始する。

    注意: `.env` に `DISCORD_BOT_TOKEN` が設定されている必要があります。
    """
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        logger.warning("DISCORD_BOT_TOKEN not set; skipping discord client start")
        return

    global _discord_task
    if _discord_task is None or _discord_task.done():
        loop = asyncio.get_running_loop()
        # client.start は永続的に動作するコルーチンなので create_task で起動する
        _discord_task = loop.create_task(discord_client.start(token))
        logger.info("started discord client task")


@app.on_event("shutdown")
async def _shutdown_discord_client():
    """FastAPI 停止時に Discord クライアントを閉じる。"""
    global _discord_task
    try:
        if discord_client.is_closed() is False:
            await discord_client.close()
            logger.info("discord client closed")
    except Exception:
        logger.exception("error while closing discord client")
    if _discord_task is not None:
        try:
            _discord_task.cancel()
        except Exception:
            pass
