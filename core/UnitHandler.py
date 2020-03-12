from typing import List

from model import Logs, Path, Player, BaseUnit, Unit, Cell
from world import World
from core.PickHandler import PickHandler


class UnitHandler:
    def __init__(self, pick_handler: PickHandler):
        super().__init__()
        self.pick_handler = pick_handler
        self.special_unit: Unit = None
        self.paths_for_my_units: List[Path] = None
        self.put_special = False
        self.standby = False

    def process(self, world: World):
        """
        """
        if self.special_unit:
            if self.special_unit.hp <= 1:
                Logs.show_log(f"restart special unit")
                self.special_unit = None
            else:
                Logs.show_log(
                    f" we have special unit now {self.special_unit.unit_id}")
        paths_for_my_units = self.choose_path(world)
        Logs.show_log(
            f"choosen paths: {[path.id for path in paths_for_my_units]}")
        self.paths_for_my_units = paths_for_my_units
        self.put_units(world, paths_for_my_units)

    def choose_path(self, world: World):
        """
        choose path and put it in self.paths_for_my_nits
        """
        if self.in_danger(world):
            Logs.show_log(f"goes in defense mode.")
            paths_for_my_units = self.defense_mode(world)
        # elif self.iam_helper(world):
        #     Logs.show_log(f"goes in helper mode.")
        #     paths_for_my_units = self.helper_mode(world)
        else:
            Logs.show_log(f"goes in attack mode.")
            paths_for_my_units = self.attack_mode(world)
        return paths_for_my_units

    def in_delta_mode(self, world: World):
        Logs.show_log(f"check for delta")
        Logs.show_log(
            f"range upgrades number {world.get_range_upgrade_number()}")
        Logs.show_log(
            f"damage upgrades number {world.get_damage_upgrade_number()}")
        option1 = world.get_range_upgrade_number(
        ) >= 2 and world.get_damage_upgrade_number() >= 1
        option2 = world.get_range_upgrade_number(
        ) >= 1 and world.get_damage_upgrade_number() >= 4
        option3 = world.get_range_upgrade_number() >= 3
        return option1 or option2 or option3

    def iam_helper(self, world: World):
        units = world.get_me().units
        if any(unit.target_if_king for unit in units):
            return None
        units = world.get_friend().units
        return any(u.target_if_king for u in units)

    def helper_mode(self, world: World):
        friend_units = world.get_friend().units
        path_for_my_units = self.attack_mode(world)
        my_paths = world.get_me().paths_from_player
        if friend_units:
            path = None
            for unit in friend_units:
                if unit.target_if_king:
                    for p in my_paths:
                        if unit.target_if_king.center in p.cells:
                            path = p
                            break
                    if path:
                        break
            path_for_my_units.append(path)
        return path_for_my_units

    def choose_units(self, world: World):
        """
        """
        myself = world.get_me()
        hand = sorted(myself.hand, key=self.pick_handler.chooser)
        return hand, myself

    def two_by_two_mode(self, world: World):
        if world.get_current_turn() % 2 == 0:
            i = 0
            myself = world.get_me()
            hand = myself.hand
            hand.sort(key=lambda u: u.ap)
            for unit in hand:
                if i == 2:
                    return
                if unit.ap <= myself.ap:
                    myself.ap -= unit.ap
                    Logs.show_log(
                        f"unit: {unit.type_id} in path: {self.paths_for_my_units[0].id}")
                    world.put_unit(
                        base_unit=unit, path=self.paths_for_my_units[0])
                    i += 1

    def units_aggregation(self, world: World):
        max_number = 0
        my_units = world.get_me().units
        path = self.paths_for_my_units[0]
        for i in range(1, len(path.cells)-1):
            unit_number = 0
            units = world.get_cell_units(path.cells[i-1])
            for unit in units:
                if unit in my_units:
                    unit_number += 1
            units = world.get_cell_units(path.cells[i])
            for unit in units:
                if unit in my_units:
                    unit_number += 1
            units = world.get_cell_units(path.cells[i+1])
            for unit in units:
                if unit in my_units:
                    unit_number += 1
            if unit_number > max_number:
                max_number = unit_number
        Logs.show_log(f"aggregation unit: {max_number}")
        return max_number

    def unit_total(self, world: World):
        unit_number = 0
        my_units = world.get_me().units
        path = self.paths_for_my_units[0]
        for cell in path.cells:
            cell_units = world.get_cell_units(cell)
            for unit in cell_units:
                if unit in my_units:
                    unit_number += 1
        Logs.show_log(f"total unit: {unit_number}")
        return unit_number

    def we_do_attack(self, world: World):
        my_units = world.get_me().units
        return any(unit.target_if_king for unit in my_units)

    def check_stand_by(self, world: World):
        Logs.show_log(f"checking for standby")
        myself = world.get_me()
        max_ap = world.get_game_constants().max_ap
        if self.in_danger(world):
            Logs.show_log(f"standby off cause of danger")
            self.standby = False
            return
        if self.we_do_attack(world):
            Logs.show_log(f"standby off cause of attack")
            self.standby = False
            return
        if myself.ap >= max_ap*0.75:
            Logs.show_log(f"standby off cause of ap {myself.ap}")
            self.standby = False
            return
        unit_aggregation = self.units_aggregation(world)
        unit_total = self.unit_total(world)
        if unit_total >= 6 and unit_aggregation >= 3:
            Logs.show_log(f"standby on")
            self.standby = True
            return
        # if unit_total < 3:
        #     Logs.show_log(f"standby off")
        #     self.standby = False
        #     return

    def put_units(self, world: World, paths_for_my_units: List[Path]):
        """
        """
        hand, myself = self.choose_units(world)
        self.check_stand_by(world)
        if self.standby:
            return
        if world.get_current_turn() < 10:
            self.two_by_two_mode(world)
            return
        # multi path
        if len(paths_for_my_units) > 1:
            Logs.show_log(f"try to put in multi path")
            hand.sort(key=lambda u: u.ap)
            its_odd_turn = world.get_current_turn() % 2
            if its_odd_turn:
                for i, path in enumerate(paths_for_my_units):
                    if i % 2:
                        for unit in hand:
                            if unit.ap <= myself.ap:
                                myself.ap -= unit.ap
                                Logs.show_log(
                                    f"unit: {unit.type_id} in path: {path.id}")
                                world.put_unit(
                                    base_unit=unit, path=path)
                                break  # put one unit
                    else:  # even path
                        continue
            else:  # even turn
                for i, path in enumerate(paths_for_my_units):
                    if not i % 2:
                        for unit in hand:
                            if unit.ap <= myself.ap:
                                myself.ap -= unit.ap
                                Logs.show_log(
                                    f"unit: {unit.type_id} in path: {path.id}")
                                world.put_unit(
                                    base_unit=unit, path=path)
                                break  # put one unit

        else:  # one path
            # special case
            if self.put_special:
                if world.get_me().units:
                    last_unit = world.get_me().units[-1]
                    self.special_unit = last_unit
                    self.put_special = False
                    Logs.show_log(
                        f" we have special unit now {self.special_unit.unit_id}")

            if self.in_delta_mode(world) and not self.special_unit:
                Logs.show_log(f"in delta mode")
                for u in hand:
                    if u.type_id == 0:
                        Logs.show_log(f" found a unit")
                        if u.ap <= myself.ap:
                            paths = self.attack_mode(world)
                            Logs.show_log(
                                f"units before put: {[unit.base_unit.type_id for unit in world.get_me().units]}")
                            world.put_unit(base_unit=u, path=paths[0])
                            self.put_special = True
                            return
                        else:
                            Logs.show_log(f"not enough ap {myself.ap}")
                            return
                if not self.put_special:
                    Logs.show_log(
                        f" not found a unit {[u.type_id for u in hand]}")
            # end of special case
            # reversed best are in the end
            for unit in reversed(hand):
                if unit.ap <= myself.ap:
                    myself.ap -= unit.ap
                    Logs.show_log(
                        f"unit: {unit.type_id} in path: {paths_for_my_units[0].id}")
                    world.put_unit(base_unit=unit, path=paths_for_my_units[0])
                    return  # one unit per turn
            Logs.show_log(f"put no unit.")

    def enemy_aggregation(self, world: World, path: Path, i, enemy_units: List[Unit]):
        unit_number = 0
        units = world.get_cell_units(path.cells[i-1])
        for unit in units:
            if unit in enemy_units:
                unit_number += 1
        units = world.get_cell_units(path.cells[i])
        for unit in units:
            if unit in enemy_units:
                unit_number += 1
        units = world.get_cell_units(path.cells[i+1])
        for unit in units:
            if unit in enemy_units:
                unit_number += 1
        return unit_number

    def in_danger(self, world: World) -> Path:
        """
        """
        paths = world.get_me().paths_from_player
        king_range = world.get_me().king.range
        units = world.get_first_enemy().units + world.get_second_enemy().units
        for path in paths:
            if self.enemy_aggregation(world, path, king_range-1, units) > 2:
                Logs.show_log(f"danger: enemy aggregation")
                return path
        for unit in units:
            if unit.target_if_king == world.get_me().king:
                for path in paths:
                    if unit.cell in path.cells:
                        Logs.show_log(f"danger: king under attack")
                        return path
        return None

    def defense_mode(self, world: World):
        """
        """
        target_path = self.in_danger(world)
        return [target_path]

    def attack_mode(self, world: World):
        """
        """
        # my paths
        my_king = world.get_me().king.center
        paths_from_me = world.get_paths_crossing_cell(cell=my_king)
        paths_to_first_enemy = []
        paths_to_second_enemy = []
        # first enemy paths
        if world.get_first_enemy().is_alive():
            first_enemy_king = world.get_first_enemy().king.center
            paths_to_first_enemy = world.get_paths_crossing_cell(
                cell=first_enemy_king)
        # second enemy paths
        if world.get_second_enemy().is_alive():
            second_enemy_king = world.get_second_enemy().king.center
            paths_to_second_enemy = world.get_paths_crossing_cell(
                cell=second_enemy_king)
        path_to_enemy = [
            path for path in paths_from_me if path in paths_to_first_enemy]
        path_to_enemy.extend(
            [path for path in paths_from_me if path in paths_to_second_enemy])
        min_path = min(path_to_enemy, key=lambda p: len(p.cells))
        path_for_my_units = [
            p for p in path_to_enemy if len(p.cells) == len(min_path.cells)
        ]
        if not path_for_my_units:
            Logs.show_log(f"error in finding path in attack mode")
        return path_for_my_units
