from fastapi import FastAPI, Request
from slack_bolt.adapter.starlette.async_handler import AsyncSlackRequestHandler

from whoopbot import app, models
from whoopbot.db import engine

models.Base.metadata.create_all(bind=engine)

app_handler = AsyncSlackRequestHandler(app)

api = FastAPI()


@api.post("/slack/events")
async def endpoint(req: Request):
    return await app_handler.handle(req)


@api.get("/slack/install")
async def install(req: Request):
    return await app_handler.handle(req)


@api.get("/slack/oauth_redirect")
async def oauth_redirect(req: Request):
    return await app_handler.handle(req)
