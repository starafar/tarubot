from box import Box
from config import settings as _settings
from datetime import datetime
from datetime import datetime, timedelta
from pony.orm import (
    Database,
    db_session,
    Optional,
    PrimaryKey,
    Required,
    set_sql_debug,
    Set,
)

from src.tarubot.api import lodestone
from typing import Union


_db = Database()

if _settings.current_env == "development":
    set_sql_debug(debug=True, show_values=True)


class Member(_db.Entity):
    discord_id = PrimaryKey(str, 20)
    characters = Set("GameCharacter", reverse="owner")

    def get_or_create(discord_id: int):
        with db_session:
            member = Member.get(discord_id=str(discord_id))

            if member is None:
                member = Member(discord_id=str(discord_id))

            return member


class GameCharacter(_db.Entity):
    char_id = PrimaryKey(str, 20)
    owner = Optional(Member, reverse="characters")
    fc = Optional("FreeCompany", reverse="members")
    forename = Required(str, 15)
    surname = Required(str, 15)
    world = Required(str, 20)

    def get_or_create(char_data: Box):
        if not char_data:
            return None

        with db_session:
            char: Union[GameCharacter, None] = GameCharacter.get(
                char_id=str(char_data.id)
            )

            if char is None:
                char = GameCharacter(
                    char_id=str(char_data.id),
                    forename=char_data.forename,
                    surname=char_data.surname,
                    world=char_data.world,
                )

            else:
                char.forename = char_data.forename
                char.surname = char_data.surname
                char.world = char_data.world

            return char


class FreeCompany(_db.Entity):
    fc_id = PrimaryKey(str, 20)
    members = Set(GameCharacter, reverse="fc")
    name = Required(str, 20)
    tag = Required(str, 5)
    world = Required(str, 20)
    gil_balance = Required(int, default=0)
    last_updated = Optional(datetime, default=datetime.min)
    guilds = Set("Guild", reverse="fc")

    async def get_or_create(fc_data: Box):
        if not fc_data:
            return None

        with db_session:
            fc = FreeCompany.get(fc_id=str(fc_data.id))

            if fc is None:
                fc = FreeCompany(
                    fc_id=str(fc_data.id),
                    name=fc_data.name,
                    tag=fc_data.tag,
                    world=fc_data.world,
                )

            else:
                fc.name = fc_data.name
                fc.tag = fc_data.tag
                fc.world = fc_data.world

            return fc


class Guild(_db.Entity):
    guild_id = PrimaryKey(str, 20)
    member_role_id = Optional(str, 20)
    guest_role_id = Optional(str, 20)
    ledger_channel_id = Optional(str, 20)
    officer_notifications_channel_id = Optional(str, 20)
    fc = Optional(FreeCompany, reverse="guilds")

    def get_or_create(guild_id: int):
        with db_session:
            guild = Guild.get(guild_id=str(guild_id))

            if guild is None:
                guild = Guild(guild_id=str(guild_id))

            return guild


match _settings.db.driver:
    case "sqlite":
        _db.bind(
            provider="sqlite",
            filename=_settings.db.sqlite.path,
            create_db=True,
        )
    case "mysql" | "maridb":
        _db.bind(
            provider="mysql",
            host=_settings.db.host,
            port=_settings.db.port or None,
            user=_settings.db.user,
            passwd=_settings.db.password,
            db=_settings.db.database,
        )
    case "postgres" | "postgresql" | "psql" | "pg" | "pgsql":
        _db.bind(
            provider="postgres",
            host=_settings.db.host,
            port=_settings.db.port or None,
            user=_settings.db.user,
            password=_settings.db.password,
            database=_settings.db.database,
        )

_db.generate_mapping(create_tables=True)
