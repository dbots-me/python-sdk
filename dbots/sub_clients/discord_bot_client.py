import asyncio
import traceback

from dbots.sub_clients.bots import BotsSubClient


class DiscordBotClient(BotsSubClient):
    def _init_discord_py(self):
        if self._autopost_enabled:
            if not self._bot:
                raise AttributeError(
                    "If you want to enable autoposting you should set the discord.py bot as bot attribute for "
                    "dbots.Client. "
                )
            self._autopost_task = self._bot.loop.create_task(self._autopost())
            self._bot.on_dbots_autpost_error = self.on_dbots_autpost_error

    async def _autopost(self):
        await self._bot.wait_until_ready()
        while not self._bot.is_closed():
            try:
                self.update_bot_stats(
                    self._bot.user.id,
                    len(self._bot.guilds),
                    shards_count=self._bot.shard_count
                    if self._post_shard_count
                    else None,
                )
                self._bot.dispatch("dbots_autpost_done")
            except Exception as e:
                self._bot.dispatch("dbots_autpost_error", e)
            await asyncio.sleep(self._autopost_interval)

    async def on_dbots_autpost_error(self, e):
        traceback.print_exception(type(e), e, e.__traceback__)
