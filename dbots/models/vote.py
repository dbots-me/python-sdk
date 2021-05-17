from datetime import datetime

from dbots.models import Model


class Vote(Model):
    id: str
    username: str
    discriminator: str
    avatar: str
    avatar_url: str
    date: datetime


class LastVotes(Model):
    votes: list[Vote]
