from typing import List

from model import Logs, Path, Player
from world import World


class UnitHandler:
    def __init__(self):
        super().__init__()

    def process(self, world: World) -> (List[Path], Player):
        """
        """
        paths_for_my_units, targeted_enemy = self.choose_path(world)
        Logs.show_log(f"chosen path {paths_for_my_units}")
        self.put_units(world, paths_for_my_units)
        return paths_for_my_units, targeted_enemy

    def choose_path(self, world: World) -> (List[Path], Player):
        """
        choose path and put it in self.paths_for_my_nits
        """
        if(world.get_friend().is_alive()):
            paths_for_my_units, targeted_enemy = self.choose_path_with_allied(
                world)
        else:
            paths_for_my_units, targeted_enemy = self.choose_path_without_allied(
                world)
        return paths_for_my_units, targeted_enemy

    def choose_path_with_allied(self, world: World) -> (List[Path], Player):
        """
        return chosen path
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
        ## Log ##
        Logs.show_log(f"my king: {my_king}")
        Logs.show_log(f"first king: {first_enemy_king}")
        Logs.show_log(f"second king: {second_enemy_king}")
        Logs.show_log(f"all path: {world.get_map().paths}")
        Logs.show_log(f"path from me: {paths_from_me}")
        Logs.show_log(f"path to first: {paths_to_first_enemy}")
        Logs.show_log(f"path to second: {paths_to_second_enemy}")
        ## Log ##
        path_to_enemy = [
            path for path in paths_from_me if path in paths_to_first_enemy]
        path_to_enemy.extend(
            [path for path in paths_from_me if path in paths_to_second_enemy])
        path_for_my_units = min(path_to_enemy, key=lambda p: len(p.cells))
        # choose targeted enemy
        if(path_for_my_units in paths_to_first_enemy):
            targeted_enemy = world.get_first_enemy()
        else:
            targeted_enemy = world.get_second_enemy()
        return [path_for_my_units], targeted_enemy

    def choose_path_without_allied(self, world: World) -> (List[Path], Player):
        """
        return chosen path
        """
        paths_for_my_units = []
        paths, targeted_enemy = self.choose_path_with_allied(world)
        paths_for_my_units.extend(paths)
        paths_for_my_units.append(world.get_me().path_to_friend)
        return paths_for_my_units, targeted_enemy

    def put_units(self, world: World, paths_for_my_units):
        """
        """
        # TODO: need refactor
        myself = world.get_me()
        for unit in myself.hand:
            if unit.ap <= myself.ap:
                world.put_unit(base_unit=unit, path=paths_for_my_units[0])
