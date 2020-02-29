from typing import List

from model import Logs, Path
from world import World


class UpgradeHandler:
    def __init__(self):
        super().__init__()

    def process(self, world: World):
        """
        """
        # this code tries to upgrade damage of first unit. in case there's no damage token, it tries to upgrade range
        myself = world.get_me()
        if world.get_range_upgrade_number or world.get_damage_upgrade_number:
            Logs.show_log(f"have upgrade.")
        if len(myself.units) > 0:
            unit = myself.units[0]
            world.upgrade_unit_damage(unit=unit)
            world.upgrade_unit_range(unit=unit)
