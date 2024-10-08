from collections.abc import Iterable
from io import BytesIO
from random import choice
from typing import TYPE_CHECKING, Any
from uuid import UUID, uuid4

from discord import Embed, Emoji, File, PartialEmoji, Reaction
from discord.ext.commands import Context as BaseContext
from discord.ext.commands import Group

from bot.constants import ERROR_REPLIES, POSITIVE_REPLIES, WARNING_REPLIES, Colours

if TYPE_CHECKING:
    from bot.bot import Xythrion


class Context(BaseContext):  # pyright: ignore[reportMissingTypeArgument]
    """Definition of a custom context."""

    bot: "Xythrion"

    async def check_subcommands(self) -> None:
        if self.invoked_subcommand is not None:
            return

        if not isinstance(self.command, Group):
            raise AttributeError("command is not a group command")

        group: Group[Any, ..., Any] = self.command

        subcommands = "\n".join(
            [f"`{cmd.name} ({", ".join(cmd.aliases)})`" if cmd.aliases else f"`{cmd.name}`" for cmd in group.commands],
        )

        await self.warning_embed(
            subcommands,
            title="Missing subcommand. Perhaps one of these?",
        )

    async def send_image_buffer(
        self,
        buffer: BytesIO,
        *,
        embed: Embed | None = None,
        file_name: str | UUID | None = None,
    ) -> None:
        embed = embed or Embed()
        file_name = file_name or uuid4()

        embed.set_image(url=f"attachment://{file_name}.png")

        file = File(fp=buffer, filename=f"{file_name}.png")

        await self.send(embed=embed, file=file)

    async def done(self, reaction: Emoji | PartialEmoji | Reaction | str = "✅") -> None:
        await self.message.add_reaction(reaction)

    @staticmethod
    def __construct_reply_embed(
        description: str,
        title: str | None,
        color: int,
        replies: Iterable[str],
    ) -> Embed:
        embed = Embed(
            title=title or choice(list(replies)),  # noqa: S311
            description=description,
            colour=color,
        )

        return embed

    async def error_embed(self, description: str, title: str | None = None) -> None:
        embed = self.__construct_reply_embed(
            description,
            title,
            Colours.soft_red,
            ERROR_REPLIES,
        )

        await self.send(embed=embed)

    async def warning_embed(self, description: str, title: str | None = None) -> None:
        embed = self.__construct_reply_embed(
            description,
            title,
            Colours.soft_orange,
            WARNING_REPLIES,
        )

        await self.send(embed=embed)

    async def success_embed(self, description: str, title: str | None = None) -> None:
        embed = self.__construct_reply_embed(
            description,
            title,
            Colours.soft_green,
            POSITIVE_REPLIES,
        )

        await self.send(embed=embed)
