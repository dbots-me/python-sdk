from datetime import datetime

from dbots.models import Model
from dbots.models.social import UserSocial


class DiscordUserFlag(Model):
    flags: int
    premium_type: int


class User(Model):
    id: str
    username: str
    discriminator: str
    avatar: str
    avatar_url: str
    status: str
    role: str
    description: str
    social: UserSocial
    bots: list[str]
    discord: DiscordUserFlag
    registered: datetime
