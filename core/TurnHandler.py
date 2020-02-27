import random
from typing import *

from core.PickHandler import PickHandler
from model import *
from world import World


class TurnHandler:
    """
    """

    def __init__(self):
        super().__init__()

    def turn(self, world: World, pick_handler: PickHandler):
        myself = world.get_me()
        max_ap = world.get_game_constants().max_ap
        path_for_my_units = pick_handler.path_for_my_units
        # play all of hand once your ap reaches maximum. if ap runs out, putUnit doesn't do anything
        if myself.ap == max_ap:
            for base_unit in myself.hand:
                world.put_unit(base_unit=base_unit, path=path_for_my_units)
        # this code tries to cast the received spell
        received_spell = world.get_received_spell()
        if received_spell is not None:
            if received_spell.is_area_spell():
                if received_spell.target == SpellTarget.ENEMY:
                    enemy_units = world.get_first_enemy().units
                    if len(enemy_units) > 0:
                        world.cast_area_spell(
                            center=enemy_units[0].cell, spell=received_spell)
                elif received_spell.target == SpellTarget.ALLIED:
                    friend_units = world.get_friend().units
                    if len(friend_units) > 0:
                        world.cast_area_spell(
                            center=friend_units[0].cell, spell=received_spell)
                elif received_spell.target == SpellTarget.SELF:
                    my_units = myself.units
                    if len(my_units) > 0:
                        world.cast_area_spell(
                            center=my_units[0].cell, spell=received_spell)
            else:  # if is unit spell
                my_units = myself.units
                if len(my_units) > 0:
                    unit = my_units[0]
                    my_paths = myself.paths_from_player
                    path = my_paths[random.randint(0, len(my_paths) - 1)]
                    size = len(path.cells)
                    cell = path.cells[int((size - 1) / 2)]
                    world.cast_unit_spell(
                        unit=unit, path=path, cell=cell, spell=received_spell)
        # this code tries to upgrade damage of first unit. in case there's no damage token, it tries to upgrade range
        if len(myself.units) > 0:
            unit = myself.units[0]
            world.upgrade_unit_damage(unit=unit)
            world.upgrade_unit_range(unit=unit)
