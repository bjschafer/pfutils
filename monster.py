import json
import math
from collections import OrderedDict


def ability_bonus(score: int) -> int:
    return math.floor((score - 10) / 2)


def increase_damage_die_step(die: str) -> str:
    die_progression = OrderedDict(

    )
    pass


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


def new_from_json(file: str) -> Monster:
    with open(file, 'r') as jsonfile:
        return json.load(jsonfile)

