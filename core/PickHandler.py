import random
from typing import List

from model import Path, Logs
from world import World


class PickHandler:
    """
    """

    def __init__(self):
        super().__init__()

    def pick(self, world: World):
        # pre process
        myself = world.get_me()
        range_factor = 2
        attack_factor = 4
        hp_factor = 1
        ap_factor = 4
        ###########

        def chooser(unit): return (
            (unit.base_range*range_factor) +
            (unit.base_attack*attack_factor) +
            (unit.max_hp*hp_factor))/3 - (unit.ap*ap_factor)
        ###########
        all_units = world.get_all_base_units()

        all_units = sorted(all_units, key=chooser)
        all_units.reverse()
        my_hand = all_units[:5]
        Logs.show_log(f"my hand: {my_hand}")
        world.choose_hand(base_units=my_hand)
        paths = world.get_me().paths_from_player
        Logs.show_log(f"Paths: {paths}")
