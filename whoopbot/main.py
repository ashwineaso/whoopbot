from dotenv import load_dotenv
from fastapi import FastAPI, Request
from mangum import Mangum

from whoopbot import models
from whoopbot.db import engine
from whoopbot.handlers import app_handler

load_dotenv()

models.Base.metadata.create_all(bind=engine)

api = FastAPI(title="Whoopbot App")


@api.post("/slack/events")
async def endpoint(req: Request):
    return await app_handler.handle(req)


@api.get("/slack/install")
async def install(req: Request):
    return await app_handler.handle(req)


@api.get("/slack/oauth_redirect")
async def oauth_redirect(req: Request):
    return await app_handler.handle(req)


handle = Mangum(api)
