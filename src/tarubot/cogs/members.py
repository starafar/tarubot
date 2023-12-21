from datetime import datetime, timedelta
from nextcord import Interaction, Member, SlashOption, slash_command
from nextcord.ext.commands import Cog
from pony.orm import db_session
from src.tarubot.api import lodestone
from src.tarubot.core import TaruBot
from src.tarubot.models.db import Guild, Member as DB_Member, GameCharacter, FreeCompany


class MemberCommands(Cog):
    def __init__(self, bot: TaruBot):
        self.bot = bot

    @slash_command(description="Assign someone a character.")
    async def assign(
        self,
        interaction: Interaction,
        member: Member = SlashOption(
            description="The member to assign a character to."
        ),
        forename: str = SlashOption(
            description="The character's forename.", max_length=15
        ),
        surname: str = SlashOption(
            description="The character's surname.", max_length=15
        ),
        world: str = SlashOption(description="The character's world.", max_length=20),
    ):
        await interaction.response.defer(with_message=True, ephemeral=True)

        with db_session:
            if not interaction.user.guild_permissions.manage_guild:
                return await interaction.send(
                    "You don't have permission to use this command.", ephemeral=True
                )

            if not member:
                return await interaction.send(
                    "You need to specify a member.", ephemeral=True
                )

            character_data = await lodestone.get_character_by_name(
                forename, surname, world
            )

            if character_data is None:
                return await interaction.send(
                    f"Unable to find `{forename} {surname}` on `{world}`.",
                    ephemeral=True,
                )

            character = GameCharacter.get_or_create(character_data)

            if character_data.fc_id:
                fc = await FreeCompany.get_or_create(
                    await lodestone.get_fc_by_id(character_data.fc_id)
                )
            else:
                fc = None

            character.fc = fc

            db_member = DB_Member.get_or_create(member.id)

            if len(db_member.characters) == 0:
                first_character = True
            else:
                first_character = False

            if character.owner == db_member:
                return await interaction.send(
                    f"`{forename} {surname}` on `{world}` is already assigned to"
                    f" {member.mention}.",
                    ephemeral=True,
                )

            if character.owner is not None:
                return await interaction.send(
                    f"`{forename} {surname}` on `{world}` is already assigned to"
                    " someone else.",
                    ephemeral=True,
                )

            character.owner = db_member

            db_guild = Guild.get_or_create(interaction.guild.id)

            if first_character:
                await member.edit(
                    nick=(
                        f"{forename} {surname}" + f" «{fc.tag}»"
                        if fc != db_guild.fc
                        else "" + f" ({world})" if world != fc.world else ""
                    )
                )

            await interaction.send(
                f"Assigned `{forename} {surname}` on `{world}` to {member.mention}.",
                ephemeral=True,
            )

        await self.bot.update_member_roles(interaction.guild.id)

    @slash_command(description="Unassign someone's character.")
    async def unassign(
        self,
        interaction: Interaction,
        member: Member = SlashOption(
            description="The member to unassign a character from."
        ),
        forename: str = SlashOption(
            description="The character's forename.", max_length=15
        ),
        surname: str = SlashOption(
            description="The character's surname.", max_length=15
        ),
        world: str = SlashOption(description="The character's world.", max_length=20),
    ):
        await interaction.response.defer(with_message=True, ephemeral=True)

        with db_session:
            if not interaction.user.guild_permissions.manage_guild:
                return await interaction.send(
                    "You don't have permission to use this command.", ephemeral=True
                )

            if not member:
                return await interaction.send(
                    "You need to specify a member.", ephemeral=True
                )

            character = GameCharacter.get_or_create(
                await lodestone.get_character_by_name(forename, surname, world)
            )

            if not character:
                return await interaction.send(
                    f"Unable to find `{forename} {surname}` on `{world}`.",
                    ephemeral=True,
                )

            if not character.owner:
                return await interaction.send(
                    f"`{forename} {surname}` on `{world}` hasn't been assigned to"
                    " anyone.",
                    ephemeral=True,
                )

            db_member = DB_Member.get_or_create(member.id)

            if character.owner != db_member:
                return await interaction.send(
                    f"`{forename} {surname}` on `{world}` is assigned to someone else.",
                    ephemeral=True,
                )

            character.owner = None

        await self.bot.update_member_roles(interaction.guild.id)

        await interaction.send(
            f"Unassigned `{forename} {surname}` on `{world}` from {member.mention}.",
            ephemeral=True,
        )

    @slash_command(description="Claim your character.")
    async def claim(
        self,
        interaction: Interaction,
        forename: str = SlashOption(
            description="Your character's forename.", max_length=15
        ),
        surname: str = SlashOption(
            description="Your character's surname.", max_length=15
        ),
        world: str = SlashOption(description="Your character's world.", max_length=20),
    ):
        await interaction.response.defer(with_message=True, ephemeral=True)

        with db_session:
            db_member = DB_Member.get_or_create(interaction.user.id)

            if len(db_member.characters) == 0:
                first_character = True
            else:
                first_character = False

            character_data = await lodestone.get_character_by_name(
                forename, surname, world
            )

            if character_data is None:
                return await interaction.send(
                    f"Unable to find `{forename} {surname}` on `{world}`.",
                    ephemeral=True,
                )

            character = GameCharacter.get_or_create(character_data)

            if character_data.fc_id:
                fc = await FreeCompany.get_or_create(
                    await lodestone.get_fc_by_id(character_data.fc_id)
                )
            else:
                fc = None

            if character.owner == db_member:
                return await interaction.send(
                    f"You've already claimed `{forename} {surname}` on `{world}`.",
                    ephemeral=True,
                )

            if character.owner is not None:
                return await interaction.send(
                    f"`{forename} {surname}` on `{world}` is claimed by someone else.",
                    ephemeral=True,
                )

            character.fc = fc
            character.owner = db_member

            db_guild = Guild.get_or_create(interaction.guild.id)

            if first_character:
                await interaction.user.edit(
                    nick=(
                        f"{forename} {surname}" + f" «{fc.tag}»"
                        if fc != db_guild.fc
                        else "" + f" ({world})" if world != fc.world else ""
                    )
                )

            await interaction.send(
                f"Claimed `{forename} {surname}` on `{world}`.",
                ephemeral=True,
            )

        await self.bot.update_member_roles(interaction.guild.id)

    @slash_command(description="Unclaim your character.")
    async def unclaim(
        self,
        interaction: Interaction,
        forename: str = SlashOption(
            description="Your character's forename.", max_length=15
        ),
        surname: str = SlashOption(
            description="Your character's surname.", max_length=15
        ),
        world: str = SlashOption(description="Your character's world.", max_length=20),
    ):
        await interaction.response.defer(with_message=True, ephemeral=True)

        with db_session:
            member = Member.get_or_create(interaction.user.id)

            if not member.characters:
                return await interaction.send(
                    "You haven't claimed any characters.", ephemeral=True
                )

            character = GameCharacter.get_or_create(
                await lodestone.get_character_by_name(forename, surname, world)
            )

            if not character:
                return await interaction.send(
                    f"Unable to find `{forename} {surname}` on `{world}`.",
                    ephemeral=True,
                )

            if not character.owner:
                return await interaction.send(
                    f"`{forename} {surname}` on `{world}` hasn't been claimed by"
                    " anyone.",
                    ephemeral=True,
                )

            if character.owner != member:
                return await interaction.send(
                    f"`{forename} {surname}` on `{world}` is claimed by someone else.",
                    ephemeral=True,
                )

            character.owner = None

        await self.bot.update_member_roles(interaction.guild.id)

        await interaction.send(
            f"Unclaimed `{forename} {surname}` on `{world}`.",
            ephemeral=True,
        )

    @slash_command(description="Refresh Free Company data.")
    async def refresh(self, interaction: Interaction):
        await interaction.response.defer(with_message=True, ephemeral=True)

        with db_session:
            guild = Guild.get_or_create(interaction.guild.id)

            if guild is None:
                return await interaction.send(
                    "This server hasn't been configured.",
                    ephemeral=True,
                )

            if not guild.fc:
                return await interaction.send(
                    "This server is not linked to a Free Company.",
                    ephemeral=True,
                )

            fc = guild.fc

            if fc.last_updated is None or fc.last_updated < datetime.now() - timedelta(
                hours=6
            ):
                fc_data = await lodestone.get_fc_members_by_id(fc.fc_id)

                if not fc_data:
                    return

                fc.members.clear()

                for member in fc_data:
                    char = GameCharacter.get_or_create(member)

                    if char:
                        fc.members.add(char)

                fc.last_updated = datetime.now()

                return await interaction.send(
                    f"Updated membership for Free Company {fc.name} «{fc.tag}» on"
                    f" {fc.world}.",
                    ephemeral=True,
                )
            else:
                return await interaction.send(
                    f"Free Company data for {fc.name} was updated recently. You can"
                    " refresh again after"
                    f" <t:{int((fc.last_updated + timedelta(hours=6)).timestamp())}:t>.",
                    ephemeral=True,
                )

    @slash_command(description="Set yourself as a guest.")
    async def guest(self, inter: Interaction):
        await inter.response.defer(thinking=True, ephemeral=True)

        with db_session:
            guild = Guild.get(guild_id=str(inter.guild.id))

            if guild is None:
                guild = Guild(guild_id=str(inter.guild.id))

            if guild.guest_role_id is None:
                await inter.followup.send(
                    "This server hasn't been configured. You'll need someone to set"
                    " your role manually.",
                    ephemeral=True,
                )
                return

            guild_object = self.bot.get_guild(int(guild.guild_id))
            guild_member = guild_object.get_member(int(inter.user.id))
            member_role = guild_object.get_role(int(guild.member_role_id))
            guest_role = guild_object.get_role(int(guild.guest_role_id))

            if member_role in guild_member.roles:
                await inter.followup.send(
                    "You're already a member. You can't be a guest at the same time.",
                    ephemeral=True,
                )
                return

            if guest_role in guild_member.roles:
                await inter.followup.send("You're already a guest.", ephemeral=True)
                return

            await guild_member.add_roles(guest_role, reason="Set as guest.")
            await inter.followup.send("Set you as a guest.", ephemeral=True)


def setup(bot: TaruBot) -> None:
    bot.add_cog(MemberCommands(bot))
