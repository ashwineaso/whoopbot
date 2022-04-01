import logging
import os

from slack_bolt.async_app import AsyncApp
from slack_bolt.oauth.async_oauth_settings import AsyncOAuthSettings

from whoopbot.auth import installation_store, oauth_state_store
from whoopbot.db import engine

logger = logging.getLogger(__name__)


installation_store.metadata.create_all(engine)
oauth_state_store.metadata.create_all(engine)

app = AsyncApp(
    logger=logger,
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
    installation_store=installation_store,
    oauth_settings=AsyncOAuthSettings(
        client_id=os.environ["SLACK_CLIENT_ID"],
        client_secret=os.environ["SLACK_CLIENT_SECRET"],
        state_store=oauth_state_store,
    ),
)
