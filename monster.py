from __future__ import annotations
import json
import math

from parser import Element

die_progression = [
    "1",
    "1d2",
    "1d3",
    "1d4",
    "1d6",
    "1d8",
    "1d10",
    "2d6",
    "2d8",
    "3d6",
    "3d8",
    "4d6",
    "4d8",
    "6d6",
    "6d8",
    "8d6",
    "8d8",
    "12d6",
    "12d8",
    "16d6"
]


def ability_bonus(score: int) -> int:
    return math.floor((score - 10) / 2)


def increase_damage_die_step(die: str) -> str:
    if die == die_progression[-1]:
        return die
    return die_progression[die_progression.index(die)+1]


class Monster:

    def _parse_ac(self):
        self.ac = self.ac.split('(')[0]
        self.normal_ac, self.touch, self.flatfooted = self.ac.split(',')
        self.touch = self.touch.split(' ')[1]
        self.flatfooted = self.flatfooted.split(' ')[1]

    def __init__(self):
        self._parse_ac()

    def augment(self):
        pass

    def giant(self):
        if self.size != 'Colossal':
            # +3 natty armor
            self.ac += 3
            self.flatfooted += 3

            self.strength += 4
            self.dexterity += -2
            self.constitution += 4

    @classmethod
    def new_from_bs(cls, page: Element) -> Monster:
        pass


def new_from_json(file: str) -> Monster:
    with open(file, 'r') as jsonfile:
        return json.load(jsonfile)

