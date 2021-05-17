from typing import Union

from dbots import HTTPClient
from dbots.models import ActionDoneModel
from dbots.models.bot import Bot
from dbots.models.bot_stats import BotStats
from dbots.models.vote import Vote
from dbots.paths.bots import (
    bot_path,
    bot_stats_path,
    bot_stats_update_path,
    last_votes_path,
    last_votes_by_user_path,
)


class BotsSubClient(HTTPClient):
    def get_bot(self, bot_id: Union[int, str]) -> Bot:
        return self.request(bot_path, bot_id=bot_id)

    def get_bot_stats(self, bot_id: Union[int, str]) -> BotStats:
        return self.request(bot_stats_path, bot_id=bot_id)

    def update_bot_stats(
        self,
        bot_id: Union[int, str],
        server_count: int,
        user_count: int = None,
        voiceconnections_count: int = None,
        shards_count: int = None,
        shard_id: int = None,
    ) -> None:
        action_done: ActionDoneModel = self.request(
            bot_stats_update_path,
            bot_id=bot_id,
            server_count=server_count,
            user_count=user_count,
            voiceconnections_count=voiceconnections_count,
            shards_count=shards_count,
            shard_id=shard_id,
        )
        assert action_done.code == 200

    def last_votes(self, bot_id: Union[int, str]) -> list[Vote]:
        return self.request(last_votes_path, bot_id=bot_id).votes

    def last_votes_by_user(
        self, bot_id: Union[int, str], user_id: Union[int, str]
    ) -> list[Vote]:
        return self.request(last_votes_by_user_path, bot_id=bot_id, user_id=user_id)
