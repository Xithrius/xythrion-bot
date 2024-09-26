import re

from discord.ext.commands import Cog

from bot.bot import Xythrion

REGEX_URL_MATCH = re.compile(r"https?://\S+")


class LinkMapEmbed(Cog):
    """Giving the link a better embed."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @staticmethod
    def get_first_url(message: str) -> str | None:
        urls = re.findall(REGEX_URL_MATCH, message)

        return urls[0] if len(urls) else None


async def setup(bot: Xythrion) -> None:
    await bot.add_cog(LinkMapEmbed(bot))
