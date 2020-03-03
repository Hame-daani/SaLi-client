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
        my_hand_ids = [0, 1, 2, 5, 6]
        world.choose_hand_by_id(type_ids=my_hand_ids)
        paths = world.get_me().paths_from_player
        Logs.show_log(f"Paths: {paths}")
