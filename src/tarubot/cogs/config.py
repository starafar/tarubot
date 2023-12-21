from nextcord import Interaction, Role, slash_command, SlashOption, TextChannel
from nextcord.ext.commands import Cog, has_guild_permissions
from pony.orm import db_session
from src.tarubot.api import lodestone
from src.tarubot.core import TaruBot
from src.tarubot.models.db import FreeCompany, Guild


class ConfigCommands(Cog):
    def __init__(self, bot: TaruBot):
        self.bot = bot

    @slash_command(description="Configure this guild.")
    @has_guild_permissions(manage_guild=True)
    async def config(self, interaction: Interaction):
        pass

    @config.subcommand()
    async def fc(self, interaction: Interaction):
        pass

    @fc.subcommand(description="Link a Free Company to this guild.")
    async def link(
        self,
        interaction: Interaction,
        fc_id: str = SlashOption(
            description="The ID of the Free Company to link to this guild.",
            max_length=20,
        ),
    ):
        if not interaction.user.guild_permissions.manage_guild:
            return await interaction.send(
                content="You do not have permission to use this command.",
                ephemeral=True,
            )

        await interaction.response.defer(with_message=True, ephemeral=True)

        with db_session:
            guild = Guild.get_or_create(interaction.guild.id)

            fc = await FreeCompany.get_or_create(await lodestone.get_fc_by_id(fc_id))

            if not fc:
                return await interaction.send(
                    content=f"Free Company {fc_id} does not exist.",
                    ephemeral=True,
                )

            if guild.fc:
                return await interaction.send(
                    content=(
                        "This guild is already linked to Free Company"
                        f" {guild.fc.name} «{guild.fc.tag}» on {guild.fc.world}."
                    ),
                    ephemeral=True,
                )

            guild.fc = fc

            await interaction.send(
                content=(
                    f"Linked Free Company {fc.name} «{fc.tag}» on {fc.world} to this"
                    " guild."
                ),
                ephemeral=True,
            )

        await self.bot.update_member_roles(interaction.guild.id)

    @fc.subcommand(description="Unlink a Free Company from this guild.")
    async def unlink(
        self,
        interaction: Interaction,
        fc_id: str = SlashOption(
            description="The ID of the Free Company to unlink from this guild.",
            max_length=20,
        ),
    ):
        await interaction.response.defer(with_message=True, ephemeral=True)

        with db_session:
            guild = Guild.get_or_create(interaction.guild.id)

            fc = await FreeCompany.get_or_create(await lodestone.get_fc_by_id(fc_id))

            if not fc:
                return await interaction.send(
                    content=f"Free Company {fc_id} does not exist.",
                    ephemeral=True,
                )

            if not guild.fc:
                return await interaction.send(
                    content=f"This guild is not linked to any Free Company.",
                    ephemeral=True,
                )

            guild.fc = None

            await interaction.followup.send(
                content=(
                    f"Unlinked Free Company {fc.name} «{fc.tag}» on {fc.world} from"
                    " this guild."
                ),
                ephemeral=True,
            )

        await self.bot.update_member_roles(interaction.guild.id)

    @config.subcommand()
    async def roles(self, interaction: Interaction):
        pass

    @roles.subcommand(description="Configure the member role for this guild.")
    async def member(
        self,
        interaction: Interaction,
        role: Role,
    ):
        await interaction.response.defer(with_message=True, ephemeral=True)

        with db_session:
            guild = Guild.get_or_create(interaction.guild.id)

            guild.member_role_id = str(role.id)

            await interaction.followup.send(
                content=f"Set member role to {role}.",
                ephemeral=True,
            )

        await self.bot.update_member_roles(interaction.guild.id)

    @roles.subcommand(description="Configure the guest role for this guild.")
    async def guest(
        self,
        interaction: Interaction,
        role: Role,
    ):
        await interaction.response.defer(with_message=True, ephemeral=True)

        with db_session:
            guild = Guild.get_or_create(interaction.guild.id)

            guild.guest_role_id = str(role.id)

            await interaction.followup.send(
                content=f"Set guest role to {role}.",
                ephemeral=True,
            )

        await self.bot.update_member_roles(interaction.guild.id)

    @config.subcommand()
    async def ledger(
        self,
        interaction: Interaction,
        channel: TextChannel = SlashOption(
            description="The channel to send ledger entries to."
        ),
    ):
        await interaction.response.defer(with_message=True, ephemeral=True)

        with db_session:
            guild = Guild.get_or_create(interaction.guild.id)

            guild.ledger_channel_id = str(channel.id)

            await interaction.followup.send(
                content=f"Set ledger channel to {channel.mention}.",
                ephemeral=True,
            )

    @config.subcommand()
    async def officer_notifications(
        self,
        interaction: Interaction,
        channel: TextChannel = SlashOption(
            description="The channel to send officer notifications to."
        ),
    ):
        await interaction.response.defer(with_message=True, ephemeral=True)

        with db_session:
            guild = Guild.get_or_create(interaction.guild.id)

            guild.officer_notifications_channel_id = str(channel.id)

            await interaction.followup.send(
                content=f"Set officer notifications channel to {channel.mention}.",
                ephemeral=True,
            )


def setup(bot: TaruBot) -> None:
    bot.add_cog(ConfigCommands(bot))
