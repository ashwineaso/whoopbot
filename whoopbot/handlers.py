import logging

from slack_bolt import App
from slack_bolt.adapter.aws_lambda.chalice_handler import ChaliceSlackRequestHandler
from slack_bolt.adapter.aws_lambda.lambda_s3_oauth_flow import LambdaS3OAuthFlow

from whoopbot.command import handle_command

# process_before_response must be True when running on FaaS
bolt_app = App(
    process_before_response=True,
    oauth_flow=LambdaS3OAuthFlow(),
)

ChaliceSlackRequestHandler.clear_all_log_handlers()
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)


@bolt_app.event("app_mention")
async def handle_app_mentions(body, say, logger):
    logger.info(body)
    await say("What's up?")


@bolt_app.event("message")
async def handle_message(body, say, logger):
    logger.info(body)
    await say("Hello!")


@bolt_app.command("/whoop")
async def command_whoop(ack, body, respond):
    await ack()
    response = await handle_command(body)
    await respond(response)
