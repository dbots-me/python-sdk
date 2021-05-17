from dbots.models import ActionDoneModel
from dbots.models.bot import Bot
from dbots.models.bot_stats import BotStats
from dbots.models.vote import LastVotes
from dbots.paths import Path

bot_path = Path("GET", "/bots/bot_id", caching=3 * 60, response_type=Bot, url_params=["bot_id"])
bot_stats_path = Path(
    "GET", "/bots/bot_id/stats", caching=60, response_type=BotStats, url_params=["bot_id"]
)
bot_stats_update_path = Path(
    "POST",
    "/bots/bot_id/stats",
    require_auth=True,
    response_type=ActionDoneModel,
    url_params=["bot_id"],
    params=[
        "server_count",
        "user_count",
        "voiceconnections_count",
        "shards_count",
        "shard_id",
    ],
)

last_votes_path = Path(
    "GET",
    "/bots/bot_id/votes",
    require_auth=True,
    caching=60,
    response_type=LastVotes,
    url_params=["bot_id"],
)

last_votes_by_user_path = Path(
    "GET",
    "/bots/bot_id/votes/user_id",
    require_auth=True,
    caching=60,
    response_type=LastVotes,
    url_params=["bot_id", "user_id"],
)
