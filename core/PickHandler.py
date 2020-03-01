import random
from typing import List

from model import Path
from world import World


class PickHandler:
    """
    """

    def __init__(self):
        super().__init__()

    def pick(self, world: World):
        # pre process
        my_hand_ids = [1, 5, 7, 8, 3]
        world.choose_hand_by_id(type_ids=my_hand_ids)
