import random
from typing import List

from model import Path, Logs, BaseUnit
from world import World


class PickHandler:
    """
    """

    def __init__(self):
        super().__init__()
        self.max_range = 0
        self.min_range = 0
        self.max_attack = 0
        self.min_attack = 0
        self.max_hp = 0
        self.min_hp = 0
        self.max_ap = 0
        self.min_ap = 0

    def chooser(self, unit): return (
        ((unit.base_range-self.min_range)*100)/(self.max_range-self.min_range) +
        ((unit.base_attack-self.min_attack)*100)/(self.max_attack-self.min_attack) +
        ((unit.max_hp-self.min_hp)*100)/(self.max_hp-self.min_hp) -
        ((unit.ap-self.min_ap)*100)/(self.max_ap-self.min_ap))

    def pick(self, world: World):
        # pre process
        all_units = world.get_all_base_units()
        self.max_range = max([u.base_range for u in all_units])
        self.min_range = min([u.base_range for u in all_units])
        self.max_attack = max([u.base_attack for u in all_units])
        self.min_attack = min([u.base_attack for u in all_units])
        self.max_hp = max([u.max_hp for u in all_units])
        self.min_hp = min([u.max_hp for u in all_units])
        self.max_ap = max([u.ap for u in all_units])
        self.min_ap = min([u.ap for u in all_units])

        all_units = sorted(all_units, key=self.chooser)
        all_units.reverse()
        my_hand = all_units[:5]
        Logs.show_log(f"my id: {world.get_me().player_id}")
        Logs.show_log(f"units: {[u.type_id for u in all_units]}")
        Logs.show_log(f"my hand: {[u.type_id for u in my_hand]}")
        world.choose_hand(base_units=my_hand)
        paths = world.get_me().paths_from_player
        Logs.show_log(f"Paths: {paths}")
