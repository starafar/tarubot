from logging import debug as log_debug
from nextcord import Interaction, slash_command, ChannelType, Embed
from nextcord.ext.commands import Cog
from pony.orm import db_session
from src.tarubot.core import TaruBot
from src.tarubot.models.db import Guild

green_symbol = "\U00002705"
yellow_symbol = "\U000026a0"
red_symbol = "\U000026d4"


class ChatCommands(Cog):
    def __init__(self, bot: TaruBot):
        self.bot = bot

    @slash_command(description="Flag this channel as GREEN.")
    async def green(self, interaction: Interaction):
        await interaction.response.defer(with_message=True, ephemeral=True)

        this_channel = self.bot.get_channel(interaction.channel.id)

        if this_channel.type != ChannelType.voice:
            return await interaction.send(
                content="This command can only be used in voice channels.",
                ephemeral=True,
            )

        if interaction.user not in this_channel.members:
            return await interaction.send(
                content="You must be in the channel to use this command.",
                ephemeral=True,
            )

        await interaction.send(
            content="This channel is now GREEN.",
            ephemeral=True,
        )

        mention_list = ", ".join(
            [member.mention for member in this_channel.members if not member.bot]
        )

        await this_channel.send(
            f"{green_symbol} This channel is now GREEN. {green_symbol}\n\n**Have"
            f" fun!**\n\n{mention_list}"
        )

        # TODO: Figure out why this is hitting the Discord API rate limit so quickly.

        # if this_channel.name[0] in [yellow_symbol, red_symbol]:
        #     await this_channel.edit(name=this_channel.name[2:])

        #     await interaction.send(
        #         content="This channel is now GREEN.",
        #         ephemeral=True,
        #     )

        #     mention_list = ", ".join(
        #         [member.mention for member in this_channel.members if not member.bot]
        #     )

        #     await this_channel.send(
        #         f"{green_symbol} This channel is now GREEN. {green_symbol}\n\n**Have"
        #         f" fun!**\n\n{mention_list}"
        #     )
        # else:
        #     await interaction.send(
        #         content="This channel is already GREEN.",
        #         ephemeral=True,
        #     )

    @slash_command(description="Flag this channel as RED.")
    async def red(self, interaction: Interaction):
        await interaction.response.defer(with_message=True, ephemeral=True)

        this_channel = self.bot.get_channel(interaction.channel.id)

        if this_channel.type != ChannelType.voice:
            return await interaction.send(
                content="This command can only be used in voice channels.",
                ephemeral=True,
            )

        if interaction.user not in this_channel.members:
            return await interaction.send(
                content="You must be in the channel to use this command.",
                ephemeral=True,
            )

        # if this_channel.name[0] == red_symbol:
        #     await interaction.send(
        #         content="This channel is already RED.",
        #         ephemeral=True,
        #     )

        # if this_channel.name[0] == yellow_symbol:
        #     await this_channel.edit(name=f"{red_symbol} {this_channel.name[2:]}")
        # else:
        #     await this_channel.edit(name=f"{red_symbol} {this_channel.name}")

        await interaction.send(
            content="This channel is now RED.",
            ephemeral=True,
        )

        mention_list = ", ".join(
            [member.mention for member in this_channel.members if not member.bot]
        )

        await this_channel.send(
            content=(
                f"{red_symbol} This channel is now RED. {red_symbol}\n\nThe current"
                " conversation is causing distress to someone in the channel. **Please"
                f" change the topic or move to another channel.**\n\n{mention_list}"
            ),
        )

        with db_session:
            db_guild = Guild.get_or_create(str(interaction.guild.id))
            officer_notifications_channel = self.bot.get_channel(
                int(db_guild.officer_notifications_channel_id)
            )

        if officer_notifications_channel:
            embed = (
                Embed(
                    title=f"Red flag warning!",
                    color=0xFF0000,
                )
                .add_field(name="User", value=interaction.user.mention)
                .add_field(name="Channel", value=this_channel.mention)
                .add_field(name="Members Present", value=mention_list)
            )

            await officer_notifications_channel.send(embed=embed)

    @slash_command(description="Flag this channel as YELLOW.")
    async def yellow(self, interaction: Interaction):
        await interaction.response.defer(with_message=True, ephemeral=True)

        this_channel = self.bot.get_channel(interaction.channel.id)

        if this_channel.type != ChannelType.voice:
            return await interaction.send(
                content="This command can only be used in voice channels.",
                ephemeral=True,
            )

        if interaction.user not in this_channel.members:
            return await interaction.send(
                content="You must be in the channel to use this command.",
                ephemeral=True,
            )

        # if this_channel.name[0] == yellow_symbol:
        #     await interaction.send(
        #         content="This channel is already YELLOW.",
        #         ephemeral=True,
        #     )

        # if this_channel.name[0] == red_symbol:
        #     await this_channel.edit(name=f"{yellow_symbol} {this_channel.name[2:]}")
        # else:
        #     await this_channel.edit(name=f"{yellow_symbol} {this_channel.name}")

        await interaction.send(
            content="This channel is now YELLOW.",
            ephemeral=True,
        )

        mention_list = ", ".join(
            [member.mention for member in this_channel.members if not member.bot]
        )

        await this_channel.send(
            content=(
                f"{yellow_symbol} This channel is now YELLOW. {yellow_symbol}\n\nThe"
                " current conversation is heading in a direction that might cause"
                " distress to someone in the channel. **Time to check in with each"
                f" other!**\n\n{mention_list}"
            ),
        )

        with db_session:
            db_guild = Guild.get_or_create(str(interaction.guild.id))
            officer_notifications_channel = self.bot.get_channel(
                int(db_guild.officer_notifications_channel_id)
            )

        if officer_notifications_channel:
            embed = (
                Embed(
                    title=f"Yellow flag warning!",
                    color=0xFFFF00,
                )
                .add_field(name="User", value=interaction.user.mention)
                .add_field(name="Channel", value=this_channel.mention)
                .add_field(name="Members Present", value=mention_list)
            )

            await officer_notifications_channel.send(embed=embed)


def setup(bot: TaruBot):
    bot.add_cog(ChatCommands(bot))
