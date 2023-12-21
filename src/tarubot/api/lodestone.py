from aiohttp import ClientSession
from box import Box
from bs4 import BeautifulSoup
from config import settings
from typing import Optional, Union
import re


def _make_character_box(
    char_id: int,
    forename: str,
    surname: str,
    world: str,
    datacenter: str,
    fc_id: Optional[int] = None,
) -> Box:
    character = Box()

    character.id: int = char_id
    character.forename: str = forename
    character.surname: str = surname
    character.world: str = world
    character.datacenter: str = datacenter
    character.fc_id: Optional[int] = fc_id

    return character


async def get_character_by_id(character_id: int) -> Union[Box, None]:
    async with ClientSession(
        headers={
            "User-Agent": "curl/7.88.1",
        }
    ) as session:
        async with session.get(
            f"https://na.finalfantasyxiv.com/lodestone/character/{character_id}/"
        ) as response:
            if response.status == 404:
                return None

            soup = BeautifulSoup(await response.text(), "html.parser")

    character_data = soup.find("div", {"class": "ldst__window"})

    if character_data is None:
        return None

    if character_data.find("div", {"class": "character__freecompany__name"}) is None:
        fc_id = None
    else:
        fc_id = int(
            character_data.find("div", {"class": "character__freecompany__name"})
            .find("a")
            .get("href")
            .split("/")[-2]
        )

    return _make_character_box(
        character_id,
        *character_data.find("p", {"class": "frame__chara__name"}).text.split(" "),
        *list(
            map(
                lambda x: x.strip(" []"),
                character_data.find("p", {"class": "frame__chara__world"}).text.split(
                    " "
                ),
            )
        ),
        fc_id,
    )


async def get_character_by_name(
    forename: str, surname: str, world: str
) -> Union[Box, None]:
    search_results = await search_characters_by_name(forename, surname, world)

    if search_results is None:
        return None

    for result in search_results:
        if (
            result.forename.lower() == forename.lower()
            and result.surname.lower() == surname.lower()
            and result.world.lower() == world.lower()
        ):
            return await get_character_by_id(result.id)

    return None


async def search_characters_by_name(
    forename: str, surname: str, world: str, _page: Optional[int] = 1
) -> Union[list[Box], None]:
    async with ClientSession(
        headers={
            "User-Agent": "curl/7.88.1",
        }
    ) as session:
        async with session.get(
            f"https://na.finalfantasyxiv.com/lodestone/character/",
            params={"q": f"{forename}+{surname}", "worldname": world, "page": _page},
        ) as response:
            if response.status == 404:
                return None

            soup = BeautifulSoup(await response.text(), "html.parser")

    search_results = soup.find("div", {"class": "ldst__window"})

    if search_results is None:
        return None

    character_list = search_results.find_all("div", {"class": "entry"})

    if character_list is None:
        return None

    result_set = []

    for character in character_list:
        result_set.append(
            _make_character_box(
                int(character.find("a").get("href").split("/")[-2]),
                *character.find("p", {"class": "entry__name"}).text.split(" "),
                *list(
                    map(
                        lambda x: x.strip(" []"),
                        character.find("p", {"class": "entry__world"}).text.split(" "),
                    )
                ),
            )
        )

    cur_page, max_page = map(
        lambda x: int(x),
        re.match(
            r"Page (\d+) of (\d+)",
            search_results.find("li", {"class": "btn__pager__current"}).text,
        ).groups(),
    )

    if cur_page < max_page:
        result_set.extend(
            await search_characters_by_name(forename, surname, world, _page + 1)
        )

    return result_set


async def get_fc_by_id(fc_id: int) -> Union[Box, None]:
    async with ClientSession(
        headers={
            "User-Agent": "curl/7.88.1",
        }
    ) as session:
        async with session.get(
            f"https://na.finalfantasyxiv.com/lodestone/freecompany/{fc_id}/"
        ) as response:
            if response.status == 404:
                return None

            soup = BeautifulSoup(await response.text(), "html.parser")

    fc_data = soup.find("div", {"class": "ldst__window"})

    if fc_data is None:
        return None

    fc = Box()

    fc.id = fc_id

    fc.name = fc_data.find("p", {"class": "entry__freecompany__name"}).text

    fc.tag = fc_data.find("p", {"class": "freecompany__text__tag"}).text.strip("«»")

    fc.world, fc.datacenter = list(
        map(
            lambda x: x.strip(" \t\n[]"),
            fc_data.select_one(
                "div.entry__freecompany__box > p:nth-child(3)"
            ).text.split(" "),
        )
    )

    return fc


async def get_fc_members_by_id(
    fc_id: int, _page: Optional[int] = 1
) -> Union[list[Box], None]:
    async with ClientSession(
        headers={
            "User-Agent": "curl/7.88.1",
        }
    ) as session:
        async with session.get(
            f"https://na.finalfantasyxiv.com/lodestone/freecompany/{fc_id}/member/",
            params={"page": _page},
        ) as response:
            if response.status == 404:
                return None

            soup = BeautifulSoup(await response.text(), "html.parser")

    fc_member_data = soup.find("div", {"class": "ldst__window"})

    if fc_member_data is None:
        return None

    fc_member_results = []

    fc_member_list = soup.find_all("li", {"class": "entry"})

    for fc_member in fc_member_list:
        fc_member_results.append(
            _make_character_box(
                int(fc_member.find("a").get("href").split("/")[-2]),
                *fc_member.find("p", {"class": "entry__name"}).text.split(" "),
                *list(
                    map(
                        lambda x: x.strip(" []"),
                        fc_member.find("p", {"class": "entry__world"}).text.split(" "),
                    )
                ),
                fc_id,
            )
        )

    cur_page, max_page = map(
        lambda x: int(x),
        re.match(
            r"Page (\d+) of (\d+)",
            fc_member_data.find("li", {"class": "btn__pager__current"}).text,
        ).groups(),
    )

    if cur_page < max_page:
        fc_member_results.extend(await get_fc_members_by_id(fc_id, _page + 1))

    return fc_member_results
