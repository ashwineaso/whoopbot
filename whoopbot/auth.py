import logging
import os
import time
from datetime import datetime
from logging import Logger
from typing import Optional
from uuid import uuid4

from databases import Database
from slack_sdk.oauth.installation_store import Bot, Installation
from slack_sdk.oauth.installation_store.async_installation_store import (
    AsyncInstallationStore,
)
from slack_sdk.oauth.installation_store.sqlalchemy import SQLAlchemyInstallationStore
from slack_sdk.oauth.state_store.async_state_store import AsyncOAuthStateStore
from slack_sdk.oauth.state_store.sqlalchemy import SQLAlchemyOAuthStateStore
from sqlalchemy import and_, desc, Table, MetaData

from whoopbot.db import SQLALCHEMY_DATABASE_URL, engine


class AsyncSQLAlchemyInstallationStore(AsyncInstallationStore):
    database_url: str
    client_id: str
    metadata: MetaData
    installations: Table
    bots: Table

    def __init__(
        self,
        client_id: str,
        database_url: str,
        logger: Logger = logging.getLogger(__name__),
    ):
        self.client_id = client_id
        self.database_url = database_url
        self._logger = logger
        self.metadata = MetaData()
        self.installations = SQLAlchemyInstallationStore.build_installations_table(
            metadata=self.metadata,
            table_name=SQLAlchemyInstallationStore.default_installations_table_name,
        )
        self.bots = SQLAlchemyInstallationStore.build_bots_table(
            metadata=self.metadata,
            table_name=SQLAlchemyInstallationStore.default_bots_table_name,
        )

    @property
    def logger(self) -> Logger:
        return self._logger

    async def async_save(self, installation: Installation):
        async with Database(self.database_url) as database:
            async with database.transaction():
                i = installation.to_dict()
                i["client_id"] = self.client_id
                await database.execute(self.installations.insert(), i)
                b = installation.to_bot().to_dict()
                b["client_id"] = self.client_id
                await database.execute(self.bots.insert(), b)

    async def async_find_bot(
        self,
        *,
        enterprise_id: Optional[str],
        team_id: Optional[str],
        is_enterprise_install: Optional[bool] = False,
    ) -> Optional[Bot]:
        c = self.bots.c
        query = (
            self.bots.select()
            .where(and_(c.enterprise_id == enterprise_id, c.team_id == team_id))
            .order_by(desc(c.installed_at))
            .limit(1)
        )
        async with Database(self.database_url) as database:
            result = await database.fetch_one(query)
            if result:
                return Bot(
                    app_id=result["app_id"],
                    enterprise_id=result["enterprise_id"],
                    team_id=result["team_id"],
                    bot_token=result["bot_token"],
                    bot_id=result["bot_id"],
                    bot_user_id=result["bot_user_id"],
                    bot_scopes=result["bot_scopes"],
                    installed_at=result["installed_at"],
                )
            else:
                return None


class AsyncSQLAlchemyOAuthStateStore(AsyncOAuthStateStore):
    database_url: str
    expiration_seconds: int
    metadata: MetaData
    oauth_states: Table

    def __init__(
        self,
        *,
        expiration_seconds: int,
        database_url: str,
        logger: Logger = logging.getLogger(__name__),
    ):
        self.expiration_seconds = expiration_seconds
        self.database_url = database_url
        self._logger = logger
        self.metadata = MetaData()
        self.oauth_states = SQLAlchemyOAuthStateStore.build_oauth_states_table(
            metadata=self.metadata,
            table_name=SQLAlchemyOAuthStateStore.default_table_name,
        )

    @property
    def logger(self) -> Logger:
        return self._logger

    async def async_issue(self) -> str:
        state: str = str(uuid4())
        now = datetime.utcfromtimestamp(time.time() + self.expiration_seconds)
        async with Database(self.database_url) as database:
            await database.execute(
                self.oauth_states.insert(), {"state": state, "expire_at": now}
            )
            return state

    async def async_consume(self, state: str) -> bool:
        try:
            async with Database(self.database_url) as database:
                async with database.transaction():
                    c = self.oauth_states.c
                    query = self.oauth_states.select().where(
                        and_(c.state == state, c.expire_at > datetime.utcnow())
                    )
                    row = await database.fetch_one(query)
                    self.logger.debug(f"consume's query result: {row}")
                    await database.execute(
                        self.oauth_states.delete().where(c.id == row["id"])
                    )
                    return True
        except Exception as e:
            message = f"Failed to find any persistent data for state: {state} - {e}"
            self.logger.warning(message)
        return False


logger = logging.getLogger(__name__)


installation_store = AsyncSQLAlchemyInstallationStore(
    client_id=os.getenv("SLACK_CLIENT_ID"),
    database_url=SQLALCHEMY_DATABASE_URL,
    logger=logger,
)
oauth_state_store = AsyncSQLAlchemyOAuthStateStore(
    expiration_seconds=120,
    database_url=SQLALCHEMY_DATABASE_URL,
    logger=logger,
)


installation_store.metadata.create_all(engine)
oauth_state_store.metadata.create_all(engine)
