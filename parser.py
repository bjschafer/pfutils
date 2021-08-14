import re
from typing import Union, Generator

import bs4.element
import pypandoc
import requests
from bs4 import BeautifulSoup, NavigableString

Element = Union[BeautifulSoup, NavigableString]

SKILLS = {"Acrobatics", "Appraise", "Bluff", "Climb", "Craft", "Diplomacy",
          "Disable Device", "Disguise", "Escape Artist", "Fly", "Handle Animal",
          "Heal", "Intimidate", "Knowledge", "Linguistics", "Perception", "Perform",
          "Profession", "Ride", "Sense Motive", "Sleight of Hand", "Spellcraft",
          "Stealth", "Survival", "Swim", "Use Magic Device"}

ABILITIES = {"Charisma", "Constitution", "Dexterity", "Intelligence", "Strength", "Wisdom"}

IGNORABLE_LINKS = {"low-light vision", "darkvision", "touch", "flat-footed", "concentration"
                   "dodge", "natural", "size", "HD", "Grapple"
                   "saving throw", "skill check",
                   "Will", "Fort", "Reflex"}
IGNORABLE_LINKS.update(SKILLS)
IGNORABLE_LINKS.update(ABILITIES)
IGNORABLE_LINKS.update({f[0:3] for f in ABILITIES})  # short names


def clean_elements(element: Element) -> Element:
    for link in element.find_all("a"):
        if link.string in IGNORABLE_LINKS:
            link.replace_with(link.string)
        if 'class' in link.attrs and 'spell' in link.attrs['class']:
            del link['class']
    for span in element.find_all("span"):
        if span.string:
            span.replace_with(span.string)
        elif span.text:
            span.replace_with(span.text)
    return element


def get_div(url: str) -> Element:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    div = soup.find("div", attrs={"class": "statblock"})
    # div = soup.find("div", attrs={"class": "article-content"})
    del div['class']
    return div


def clean_url(url: str) -> str:
    div = get_div(url)
    if not div:
        return ""
    clean_div = clean_elements(div)
    return clean_div


def url_to_md(url: str) -> str:
    clean_div = clean_url(url)
    converted = pypandoc.convert_text(clean_div, "gfm", format="html", extra_args=["--wrap=none"])
    return re.sub(r"<\/?div.*>", "", converted)


def parse_monster(url: str, no_convert: bool) -> Generator[str, None, None]:
    if 'monster-listings' in url:
        if no_convert:
            yield clean_url(url)
        else:
            yield url_to_md(url)
    else:
        monster_list = BeautifulSoup(
            requests.get(url).content, 'html.parser')

        def is_monster_link(tag: bs4.element.Tag) -> bool:
            if tag.name == "a":
                link: str = tag.get('href')
                if link and 'monster-listings' in link and 'templates' not in link:
                    return True
            return False

        monster_links = monster_list.find_all(is_monster_link)
        for url_obj in monster_links:
            if no_convert:
                yield clean_url(url)
            else:
                yield url_to_md(url_obj['href'])
