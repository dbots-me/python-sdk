from datetime import datetime
from json import loads
from typing import Union

import requests
from requests.auth import AuthBase

from dbots.cache import Cache, CacheConfiguration
from dbots.errors import handle_response, AuthenticationNeeded
from dbots.paths import Path


class DBotsAuthentication(AuthBase):
    def __init__(self, bot_token: str):
        self._bot_token = bot_token

    def __call__(self, r: requests.Request):
        r.headers["Authorization"] = self._bot_token
        return r


class HTTPClient:
    def __init__(
        self,
        bot_token: str = None,
        bot=None,
        autopost_enabled: bool = False,
        autopost_interval: int = 15 * 60,
        post_shard_count: bool=True,
        base_url: str = "https://api.dbots.me/v1",
        cache=None,
        disable_cache=False,
    ):
        if base_url.endswith("/"):
            base_url = base_url[:-1]
        if not cache:
            if disable_cache:
                cache = Cache(CacheConfiguration.DISABLED)
            else:
                cache = Cache(CacheConfiguration.MEMORY)
        self._cache = cache
        self._base_url = base_url
        if bot_token:
            self._auth = DBotsAuthentication(bot_token)
        else:
            self._auth = None

        self._bot = bot
        self._autopost_enabled = autopost_enabled
        self._autopost_interval = autopost_interval
        self._post_shard_count = post_shard_count
        if hasattr(self, "_init_discord_py"):
            self._init_discord_py()
        else:
            print(self)

    def request(self, path: Path, **kwargs):
        requests_args, requests_kwargs = path.build(self._base_url, **kwargs)
        if path.caching:
            cached_value = self._cache.read_cache(requests_args[1])
            if cached_value:
                return path.response_type.from_dict(loads(cached_value))
        if path.require_auth:
            if not self._auth:
                raise AuthenticationNeeded()
            requests_kwargs["auth"] = self._auth
        response = requests.request(*requests_args, **requests_kwargs)
        j = handle_response(response)
        if path.response_type:
            d = path.response_type.from_dict(j)
            if path.caching:
                self._cache.add_cache(
                    requests_args[1],
                    j,
                    datetime.fromisoformat(j["cache_date"]),
                    path.caching,
                )
            return d
        else:
            return j
