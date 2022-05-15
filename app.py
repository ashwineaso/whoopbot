import logging

from chalice import Chalice, Response
from slack_bolt.adapter.aws_lambda.chalice_handler import ChaliceSlackRequestHandler

from whoopbot.handlers import bolt_app

ChaliceSlackRequestHandler.clear_all_log_handlers()
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

# Don't change this variable name "app"
app = Chalice(app_name="whoopbot")
slack_handler = ChaliceSlackRequestHandler(app=bolt_app, chalice=app)


@app.route(
    "/slack/events",
    methods=["POST"],
    content_types=["application/x-www-form-urlencoded", "application/json"],
)
def events() -> Response:
    return slack_handler.handle(app.current_request)


@app.route("/slack/install", methods=["GET"])
def install() -> Response:
    return slack_handler.handle(app.current_request)


@app.route("/slack/oauth_redirect", methods=["GET"])
def oauth_redirect() -> Response:
    return slack_handler.handle(app.current_request)

# configure aws credentials properly
# pip install -r requirements.txt
# cp -p .chalice/config.json .chalice/config.json
# # edit .chalice/config.json
# chalice deploy

# for local dev
# chalice local --stage dev --port 3000
