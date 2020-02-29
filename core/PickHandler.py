import random
from typing import List

from model import Path
from world import World
from model import *

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
        #-----------------------------------
        self.My_Player = world.get_me()
        self.My_First_Enemy = world.get_first_enemy()
        self.My_Second_Enemy = world.get_second_enemy()
        self.My_Freind = world.get_friend()
        #------------------------------------
        # choosing all flying units
        all_base_units = world.get_all_base_units()
        my_hand = [
            base_unit for base_unit in all_base_units if base_unit.is_flying]
        # picking the chosen hand - rest of the hand will automatically be filled with random base_units
        world.choose_hand(base_units=my_hand)
        # other pre process
        self.path_for_my_units = world.get_first_enemy().paths_from_player
        self.path_for_my_units.append(
            world.get_second_enemy().paths_from_player)
