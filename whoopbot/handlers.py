from slack_bolt.adapter.starlette.async_handler import AsyncSlackRequestHandler

from whoopbot.command import handle_command
from whoopbot.whoopbot import app


@app.event("app_mention")
async def handle_app_mentions(body, say, logger):
    logger.info(body)
    await say("What's up?")


@app.event("message")
async def handle_message(body, say, logger):
    logger.info(body)
    await say("Hello!")


@app.command("/whoop")
async def command_whoop(ack, body, respond):
    await ack()
    response = await handle_command(body)
    await respond(response)


app_handler = AsyncSlackRequestHandler(app)
