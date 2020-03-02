from typing import List

from model import Logs, Path, Player
from world import World


class UnitHandler:
    def __init__(self):
        super().__init__()

    def process(self, world: World) -> (List[Path], Player):
        """
        """
        paths_for_my_units = self.choose_path(world)
        self.put_units(world, paths_for_my_units)
        return paths_for_my_units, None

    def choose_path(self, world: World):
        """
        choose path and put it in self.paths_for_my_nits
        """
        if self.in_danger(world):
            Logs.show_log(f"goes in defense mode.")
            paths_for_my_units = self.defense_mode(world)
        # elif len(paths_for_my_units) > 1:  # friend died!
        #     self.delta_mode(world, paths_for_my_units)
        elif self.friend_in_danger(world):
            Logs.show_log(f"goes in allied mode.")
            paths_for_my_units = self.allied_mode(world)
        else:

            Logs.show_log(f"goes in attack mode.")
            paths_for_my_units = self.attack_mode(
                world, paths_for_my_units)
        return paths_for_my_units

    def choose_units(self, world: World):
        """
        """
        myself = world.get_me()
        range_factor = 1
        attack_factor = 4
        hp_factor = 1
        ap_factor = 4
        ###########

        def chooser(unit): return (
            (unit.base_range*range_factor) +
            (unit.base_attack*attack_factor) +
            (unit.max_hp*hp_factor))/3 - (unit.ap*ap_factor)
        ###########
        hand = sorted(myself.hand, key=chooser)
        return hand, myself

    def put_units(self, world: World, paths_for_my_units):
        """
        """
        hand, myself = self.choose_units(world)
        # reversed
        for unit in reversed(hand):
            if unit.ap <= myself.ap:
                myself.ap -= unit.ap
                Logs.show_log(f"unit: {unit}\npath: {paths_for_my_units[0]}")
                world.put_unit(base_unit=unit, path=paths_for_my_units[0])

    def friend_in_danger(self, world: World):
        """
        """
        if world.get_friend().king.target_cell:
            return True
        return False

    def allied_mode(self, world: World):
        """
        """
        target_cell = world.get_friend().king.target_cell
        paths = world.get_friend().paths_from_player
        target_path = None
        for path in paths:
            if target_cell in path.cells:
                target_path = path
                break
        return [target_path]

    def in_danger(self, world: World):
        """
        """
        enemy_units = world.get_first_enemy().units
        enemy_units.extend(world.get_second_enemy().units)
        for path in world.get_me().paths_from_player:
            # units in cell 8 => king.range+2
            # to be perepared
            cell_units = world.get_cell_units(path.cells[7])
            cell_units.extend(world.get_cell_units(path.cells[6]))
            if any(unit in cell_units for unit in enemy_units):
                return True
        return False

    def defense_mode(self, world: World):
        """
        """
        target_cell = world.get_me().king.target_cell
        if not target_cell:
            enemy_units = world.get_first_enemy().units
            enemy_units.extend(world.get_second_enemy().units)
            for path in world.get_me().paths_from_player:
                # units in cell 7 and 8 => king.range+2
                # to be perepared
                cell_units = world.get_cell_units(path.cells[7])
                cell_units.extend(world.get_cell_units(path.cells[6]))
                if any(unit in cell_units for unit in enemy_units):
                    target_path = path
                    break
        else:
            paths = world.get_me().paths_from_player
            target_path = None
            for path in paths:
                if target_cell in path.cells:
                    target_path = path
                    break
        return [target_path]

    def attack_mode(self, world: World, paths_for_my_units):
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
        path_for_my_units = min(path_to_enemy, key=lambda p: len(p.cells))
        return [path_for_my_units]

    def delta_mode(self, world: World, paths_for_my_units):
        """"""
        pass
