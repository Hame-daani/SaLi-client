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
        self.unit_handler = UnitHandler(pick_handler=self.pick_handler)
        self.spell_handler: SpellHandler = None
        self.upgrade_handler: UpgradeHandler = None
        self.spells: List[Spell] = []

    def turn(self, world: World):
        """
        """
        # Process Unit Puting
        self.unit_handler.process(world)

        # Process Spell Puting
        self.spell_handler = SpellHandler(
            unit_handler=self.unit_handler, splls=self.spells)
        spell = self.spell_handler.process(world)
        if spell:
            self.spells.append(spell)

        # Process Upgrades
        self.upgrade_handler = UpgradeHandler(unit_handler=self.unit_handler)
        self.upgrade_handler.process(world)
