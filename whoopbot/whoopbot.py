import logging
import os

from dotenv import load_dotenv
from slack_bolt.async_app import AsyncApp
from slack_bolt.oauth.async_oauth_settings import AsyncOAuthSettings

from whoopbot.auth import installation_store, oauth_state_store

logger = logging.getLogger(__name__)

load_dotenv()

app = AsyncApp(
    logger=logger,
    signing_secret=os.getenv("SLACK_SIGNING_SECRET"),
    installation_store=installation_store,
    oauth_settings=AsyncOAuthSettings(
        client_id=os.getenv("SLACK_CLIENT_ID"),
        client_secret=os.getenv("SLACK_CLIENT_SECRET"),
        state_store=oauth_state_store,
    ),
)
