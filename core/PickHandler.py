import random

from model import *
from world import World


def pick(ai, world: World):
    # pre process
    map = world.get_map()
    ai.rows = map.row_num
    ai.cols = map.col_num
    # choosing all flying units
    all_base_units = world.get_all_base_units()
    my_hand = [base_unit for base_unit in all_base_units if base_unit.is_flying]
    # picking the chosen hand - rest of the hand will automatically be filled with random base_units
    world.choose_hand(base_units=my_hand)
    # other pre process
    ai.path_for_my_units = world.get_friend().paths_from_player[0]
