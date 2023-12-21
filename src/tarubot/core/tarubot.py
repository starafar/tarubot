from config import settings
from nextcord import Intents, Interaction
from nextcord.ext.commands import AutoShardedBot, errors
from pony.orm import db_session
from src.tarubot.models.db import Member, Guild
import logging


class TaruBot(AutoShardedBot):
    def __init__(self, **kwargs):
        intents = Intents.none()
        intents.guilds = True
        intents.members = True
        intents.voice_states = True

        super().__init__(
            intents=intents,
            default_guild_ids=settings.get("test_guild_ids"),
            **kwargs,
        )

        self.load_extensions_from_module("src.tarubot.cogs")

    async def on_ready(self):
        logging.info(f"{self.user} is ready!")

    async def on_slash_command_error(
        self,
        interaction: Interaction,
        exception: Exception,
    ):
        match type(exception):
            case errors.MissingPermissions:
                await interaction.send(
                    content="You do not have permission to use this command.",
                    ephemeral=True,
                )

            case _:
                raise exception

    async def update_member_roles(self, guild_id: int):
        discord_guild = self.get_guild(guild_id)

        with db_session:
            guild = Guild.get_or_create(str(guild_id))

            if guild is None:
                return

            if guild.fc is None:
                return

            for discord_member in discord_guild.members:
                if discord_member.bot:
                    continue

                member = Member.get_or_create(discord_id=str(discord_member.id))

                if member is None:
                    continue

                if member.characters is None:
                    continue

                is_member = False

                for character in member.characters:
                    if character.fc is None:
                        continue

                    if character.fc.guilds is None:
                        continue

                    if guild in character.fc.guilds:
                        is_member = True
                        break

                if is_member:
                    if not guild.member_role_id or not guild.guest_role_id:
                        continue

                    member_role = discord_guild.get_role(int(guild.member_role_id))
                    guest_role = discord_guild.get_role(int(guild.guest_role_id))

                    if not member_role or not guest_role:
                        continue

                    if member_role not in discord_member.roles:
                        await discord_member.add_roles(member_role)
                    if guest_role in discord_member.roles:
                        await discord_member.remove_roles(guest_role)

                else:
                    if not guild.member_role_id or not guild.guest_role_id:
                        continue

                    member_role = discord_guild.get_role(int(guild.member_role_id))
                    guest_role = discord_guild.get_role(int(guild.guest_role_id))

                    if not member_role or not guest_role:
                        continue

                    if guest_role not in discord_member.roles:
                        await discord_member.add_roles(guest_role)
                    if member_role in discord_member.roles:
                        await discord_member.remove_roles(member_role)
