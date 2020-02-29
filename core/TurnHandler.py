import random
from typing import List

from core.PickHandler import PickHandler
from core.SpellHandler import SpellHandler
from core.UnitHandler import UnitHandler
from model import Cell, Logs, Path, Player, Spell, SpellTarget, SpellType, Unit
from world import World


class TurnHandler:
    """
    """

    def __init__(self, pick_handler: PickHandler):
        """
        """
        super().__init__()
        self.pick_handler = pick_handler
        self.paths_for_my_units: List[Path] = None
        self.targeted_enemy: Player = None
        self.unit_handler: UnitHandler = None
        self.spell_handler: SpellHandler = None

    def turn(self, world: World):
        """
        """
        # Process Unit Puting
        self.unit_handler = UnitHandler()
        self.paths_for_my_units, self.targeted_enemy = self.unit_handler.process(
            world)

        # Process Spell Puting
        self.spell_handler = SpellHandler(
            paths_for_my_units=self.paths_for_my_units, targeted_enemy=self.targeted_enemy)
        self.spell_handler.process(world)

        # Process Upgrades
        self.upgrade_process(world)

    def upgrade_process(self, world: World):
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
