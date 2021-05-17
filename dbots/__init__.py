from dbots.cache import Cache, CacheConfiguration
from dbots.httpclient import HTTPClient
from dbots.sub_clients.bots import BotsSubClient
from dbots.sub_clients.discord_bot_client import DiscordBotClient
from dbots.sub_clients.users import UsersSubClient


class Client(UsersSubClient, DiscordBotClient):
    pass
