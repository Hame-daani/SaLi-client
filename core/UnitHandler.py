from typing import List

from model import Logs, Path, Player, BaseUnit, Unit
from world import World
from core.PickHandler import PickHandler


class UnitHandler:
    def __init__(self, pick_handler: PickHandler, special_unit: Unit):
        super().__init__()
        self.pick_handler = pick_handler
        self.special_unit = special_unit

    def process(self, world: World) -> List[Path]:
        """
        """
        paths_for_my_units = self.choose_path(world)
        Logs.show_log(
            f"choosen paths: {[path.id for path in paths_for_my_units]}")
        self.put_units(world, paths_for_my_units)
        return paths_for_my_units, self.special_unit

    def choose_path(self, world: World):
        """
        choose path and put it in self.paths_for_my_nits
        """
        if self.in_danger(world):
            Logs.show_log(f"goes in defense mode.")
            paths_for_my_units = self.defense_mode(world)
        elif self.iam_helper(world):
            Logs.show_log(f"goes in helper mode.")
            paths_for_my_units = self.helper_mode(world)
        else:
            Logs.show_log(f"goes in attack mode.")
            paths_for_my_units = self.attack_mode(world)
        return paths_for_my_units

    def in_delta_mode(self, world: World):
        Logs.show_log(f"upgrades number {world.get_range_upgrade_number()}")
        return world.get_range_upgrade_number() >= 3

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

    def put_units(self, world: World, paths_for_my_units: List[Path]):
        """
        """
        hand, myself = self.choose_units(world)
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
            if world.get_me().units:
                last_unit = world.get_me().units[-1]
            if self.in_delta_mode(world) and not self.special_unit and last_unit.base_unit.type_id == 0:
                self.special_unit = last_unit
                Logs.show_log(
                    f" we have special unit now {self.special_unit.unit_id}")

            if self.in_delta_mode(world) and not self.special_unit:
                Logs.show_log(f"in delta mode")
                for u in hand:
                    if u.type_id == 0:
                        Logs.show_log(f" found zero type unit")
                        if u.ap <= myself.ap:
                            paths = self.attack_mode(world)
                            Logs.show_log(
                                f"units before put: {[unit.base_unit.type_id for unit in world.get_me().units]}")
                            world.put_unit(base_unit=u, path=paths[0])
                            break
                        else:
                            Logs.show_log(f"not enough ap {myself.ap}")
                            return
                if not self.special_unit:
                    Logs.show_log(
                        f" not found a zero type unit {[u.type_id for u in hand]}")
            # end of special case
            # reversed best are in the end
            for unit in reversed(hand):
                if unit.ap <= myself.ap:
                    myself.ap -= unit.ap
                    Logs.show_log(
                        f"unit: {unit.type_id} in path: {paths_for_my_units[0].id}")
                    world.put_unit(base_unit=unit, path=paths_for_my_units[0])
                    turn = world.get_current_turn()
                    if turn != 1:
                        return  # one unit per turn
            Logs.show_log(f"put no unit.")

    def in_danger(self, world: World) -> Path:
        """
        """
        paths = world.get_me().paths_from_player
        if world.get_me().king.target_cell:
            target_cell = world.get_me().king.target_cell
            Logs.show_log(f"king under danger {target_cell}")
            for path in paths:
                if target_cell in path.cells:
                    return path
        # TODO: when we are under attack
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
        # first enemy paths
        first_enemy_king = world.get_first_enemy().king.center
        paths_to_first_enemy = world.get_paths_crossing_cell(
            cell=first_enemy_king)
        # second enemy paths
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
        return path_for_my_units
