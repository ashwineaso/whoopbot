from whoopbot import app
from whoopbot.command import handle_command


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
