from collections.abc import Callable
from typing import Any

from discord.ext.commands import CheckFailure, check
from httpx import Response

from bot.context import Context


class TrustedUserCheckFailure(CheckFailure):
    """User is not in the trusted database, and therefore cannot run a command."""


def is_trusted() -> Callable[..., Any]:  # pragma: no cover
    async def predicate(ctx: Context) -> bool:
        if await ctx.bot.is_owner(ctx.author):
            return True

        response: Response = await ctx.bot.internal_api_client.get(
            f"/api/trusted/{ctx.author.id}",
        )

        if response.is_success:
            return True

        if response.status_code == 404:
            raise TrustedUserCheckFailure

        raise Exception("Issue when requesting to the internal trusted API endpoint")

    return check(predicate)
