from datetime import datetime

from dbots.models import Model


class BotStats(Model):
    id: str
    server_count: int
    user_count: int
    voiceconnections_count: int
    shards_count: int
    shards: list[str]
    bot_status: str
    bot_lastseen: datetime
    bot_lastfetch: datetime
    votes: int
    monthlyvotes: int