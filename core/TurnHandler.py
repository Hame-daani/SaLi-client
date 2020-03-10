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
        self.unit_handler: UnitHandler = None
        self.spell_handler: SpellHandler = None
        self.upgrade_handler: UpgradeHandler = None
        self.spells: List[Spell] = []

    def turn(self, world: World):
        """
        """
        # Process Unit Puting
        self.unit_handler = UnitHandler(pick_handler=self.pick_handler)
        self.paths_for_my_units = self.unit_handler.process(world)

        # Process Spell Puting
        self.spell_handler = SpellHandler(
            paths_for_my_units=self.paths_for_my_units, splls=self.spells)
        spell = self.spell_handler.process(world)
        if spell:
            self.spells.append(spell)

        # Process Upgrades
        self.upgrade_handler = UpgradeHandler(paths_for_my_units=self.paths_for_my_units)
        self.upgrade_handler.process(world)
