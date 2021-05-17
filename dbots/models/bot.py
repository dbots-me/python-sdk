from datetime import datetime

from dbots.models import Model
from dbots.models.tag import Tag


class Bot(Model):
    id: str
    username: str
    discriminator: str
    avatar: str
    avatar_url: str
    status: str
    custombotname: str
    nsfw: bool
    certified: bool
    partnered: bool
    owners: list[str]
    tags: list[Tag]
    prefix: str
    invite: str
    website: str
    repository: str
    supportdiscord: str
    supportdiscord_url: str
    cardbackground: str
    shortdesc: str
    longdesc: str
    registered: datetime
    cache_date: datetime
