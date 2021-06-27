import sys
from typing import Union

import bs4.element
from bs4 import BeautifulSoup, NavigableString
import pypandoc
import requests

Element = Union[BeautifulSoup, NavigableString]

skills = {"Acrobatics", "Appraise", "Bluff", "Climb", "Craft", "Diplomacy",
          "Disable Device", "Disguise", "Escape Artist", "Fly", "Handle Animal",
          "Heal", "Intimidate", "Knowledge", "Linguistics", "Perception", "Perform",
          "Profession", "Ride", "Sense Motive", "Sleight of Hand", "Spellcraft",
          "Stealth", "Survival", "Swim", "Use Magic Device"}

abilities = {"Charisma", "Constitution", "Dexterity", "Intelligence", "Strength", "Wisdom"}

ignorable_links = {"low-light vision", "darkvision", "touch", "flat-footed", "concentration"
                   "dodge", "natural", "size", "HD", "saving throw", "skill check",
                   "Will", "Fort", "Reflex"}
ignorable_links.update(skills)
ignorable_links.update(abilities)
ignorable_links.update({f[0:3] for f in abilities})  # short names


def clean_elements(element: Element) -> Element:
    for link in element.find_all("a"):
        if link.string in ignorable_links:
            link.replace_with(link.string)
        if 'class' in link.attrs and 'spell' in link.attrs['class']:
            del link['class']
    for span in element.find_all("span"):
        span.replace_with(span.string)
    return element


def get_div(url: str) -> Element:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    div = soup.find("div", attrs={"class": "statblock"})
    del div['class']
    return div


def url_to_md(url: str) -> str:
    div = get_div(url)
    if not div:
        return ""
    clean_div = clean_elements(div)
    return pypandoc.convert_text(clean_div, "markdown_github", format="html").replace("<div>", "").replace("</div>", "")


# pull down the page list
monster_list = BeautifulSoup(requests.get('https://www.d20pfsrd.com/feats/general-feats/expanded-summon-monster/').content, 'html.parser')


def is_monster_link(tag: bs4.element.Tag) -> bool:
    if tag.name == "a":
        link: str = tag.get('href')
        if link and 'monster-listings' in link and 'templates' not in link:
            return True
    return False


monster_links = monster_list.find_all(is_monster_link)
for url_obj in monster_links:
    print(url_to_md(url_obj['href']))
    sys.exit(0)
