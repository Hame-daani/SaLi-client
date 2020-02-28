import random
from typing import *

from model import *
from world import World


class PickHandler:
    """
    """

    def __init__(self):
        super().__init__()

    def pick(self, world: World):
        # pre process
        map = world.get_map()
        self.rows = map.row_num
        self.cols = map.col_num
        # choosing all flying units
        all_base_units = world.get_all_base_units()
        my_hand = [
            base_unit for base_unit in all_base_units if base_unit.is_flying]
        # picking the chosen hand - rest of the hand will automatically be filled with random base_units
        world.choose_hand(base_units=my_hand)
        # other pre process
        self.path_for_my_units = world.get_first_enemy().paths_from_player
        self.path_for_my_units.append(world.get_second_enemy().paths_from_player)
