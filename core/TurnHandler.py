import random
from typing import List

from core.PickHandler import PickHandler
from core.SpellHandler import SpellHandler
from core.UnitHandler import UnitHandler
from core.UpgradeHandler import UpgradeHandler
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
        self.upgrade_handler: UpgradeHandler = None

    def turn(self, world: World):
        """
        """
        # Process Unit Puting
        self.unit_handler = UnitHandler()
        p, t = self.unit_handler.process(world)
        self.paths_for_my_units, self.targeted_enemy = p, t

        # Process Spell Puting
        self.spell_handler = SpellHandler(
            paths_for_my_units=self.paths_for_my_units, targeted_enemy=self.targeted_enemy)
        self.spell_handler.process(world)

        # Process Upgrades
        self.upgrade_handler = UpgradeHandler()
        self.upgrade_handler.process(world)
