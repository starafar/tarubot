from nextcord import Interaction, slash_command
from nextcord.ext.commands import Cog
from src.tarubot.core import TaruBot


class UtilityCommands(Cog):
    def __init__(self, bot: TaruBot):
        self.bot = bot

    @slash_command(description="Pong!")
    async def ping(self, interaction: Interaction):
        await interaction.send(
            "Pong! Current API latency is"
            f" {round(self.bot.latency * 1000)} milliseconds.",
            ephemeral=True,
        )

    @slash_command(description="Get channel information.")
    async def channel(self, interaction: Interaction):
        await interaction.send(
            f"Channel ID: {interaction.channel.id}\nChannel Name:"
            f" {interaction.channel.name}\nChannel Type: {interaction.channel.type}",
            ephemeral=True,
        )


def setup(bot: TaruBot):
    bot.add_cog(UtilityCommands(bot))
