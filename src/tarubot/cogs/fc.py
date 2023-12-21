from config import settings
from nextcord import Interaction, Embed, slash_command, SlashOption
from nextcord.ext.commands import Cog, has_guild_permissions
from pony.orm import db_session
from src.tarubot.core import TaruBot
from src.tarubot.models.db import Guild


class FreeCompanyCommands(Cog):
    def __init__(self, bot: TaruBot):
        self.bot = bot

    @slash_command(description="Add an entry to the FC ledger.")
    async def ledger(self, interaction: Interaction):
        pass

    @ledger.subcommand(description="Add a deposit entry to the FC ledger.")
    async def deposit(
        self,
        interaction: Interaction,
        amount: int = SlashOption(
            description="The amount of gil to deposit.",
            min_value=1,
            max_value=999999999,
        ),
        note: str = SlashOption(description="A note to add to the ledger entry."),
    ):
        if amount == 0:
            await interaction.send("Please enter a non-zero amount.", ephemeral=True)
            return

        await interaction.response.defer(with_message=True, ephemeral=True)

        with db_session:
            guild = Guild.get_or_create(guild_id=str(interaction.guild.id))

            if not guild.fc:
                await interaction.send(
                    "This Discord server is not linked to a Free Company.",
                    ephemeral=True,
                )
                return

            guild.fc.gil_balance += amount

            ledger_channel = self.bot.get_channel(guild.ledger_channel_id)

            embed = (
                Embed(
                    title=f"Deposit",
                    color=0x007F00,
                )
                .add_field(name="User", value=interaction.author.mention, inline=True)
                .add_field(name="Amount", value=f"{amount:,}", inline=True)
                .add_field(name="Note", value=note, inline=True)
                .add_field(name="Balance", value=f"{guild.fc.gil_balance:,}")
            )

        await ledger_channel.send(embed=embed)

        await interaction.send("Entry added to the ledger.", ephemeral=True)

    @ledger.subcommand(description="Add a withdrawal entry to the FC ledger.")
    @has_guild_permissions(manage_guild=True)
    async def withdraw(
        self,
        interaction: Interaction,
        amount: int = SlashOption(
            description="The amount of gil to withdraw.",
            min_value=1,
            max_value=999999999,
        ),
        note: str = SlashOption(description="A note to add to the ledger entry."),
    ):
        if amount == 0:
            await interaction.send("Please enter a non-zero amount.", ephemeral=True)
            return

        await interaction.response.defer(with_message=True, ephemeral=True)

        with db_session:
            guild = Guild.get_or_create(guild_id=str(interaction.guild.id))

            if not guild.fc:
                await interaction.send(
                    "This Discord server is not linked to a Free Companies.",
                    ephemeral=True,
                )
                return

            if guild.fc.gil_balance < amount:
                await interaction.send(
                    "The FC does not have enough gil to withdraw that amount.",
                    ephemeral=True,
                )
                return

            guild.fc.gil_balance -= amount

            ledger_channel = self.bot.get_channel(guild.ledger_channel_id)

            embed = (
                Embed(
                    title=f"Withdrawal",
                    color=0x7F0000,
                )
                .add_field(name="User", value=interaction.author.mention, inline=True)
                .add_field(name="Amount", value=f"{amount:,}", inline=True)
                .add_field(name="Note", value=note, inline=True)
                .add_field(name="Balance", value=f"{guild.fc.gil_balance:,}")
            )

        await ledger_channel.send(embed=embed)

        await interaction.send("Entry added to the ledger.", ephemeral=True)


def setup(bot: TaruBot):
    bot.add_cog(FreeCompanyCommands(bot))
