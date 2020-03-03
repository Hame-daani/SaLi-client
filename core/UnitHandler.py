from typing import List

from model import Logs, Path, Player, BaseUnit
from world import World


class UnitHandler:
    def __init__(self):
        super().__init__()

    def process(self, world: World) -> List[Path]:
        """
        """
        paths_for_my_units = self.choose_path(world)
        Logs.show_log(
            f"choosen paths: {[path.id for path in paths_for_my_units]}")
        self.put_units(world, paths_for_my_units)
        return paths_for_my_units

    def choose_path(self, world: World):
        """
        choose path and put it in self.paths_for_my_nits
        """
        if self.fucked_up(world):
            Logs.show_log(f"goes in delta mode.")
            paths_for_my_units = self.delta_mode(world)
        elif self.in_danger(world):
            Logs.show_log(f"goes in defense mode.")
            paths_for_my_units = self.defense_mode(world)
        elif self.friend_in_danger(world):
            Logs.show_log(f"goes in allied mode.")
            paths_for_my_units = self.allied_mode(world)
        else:

            Logs.show_log(f"goes in attack mode.")
            paths_for_my_units = self.attack_mode(world)
        return paths_for_my_units

    def choose_units(self, world: World):
        """
        """
        myself = world.get_me()
        range_factor = 2
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

    def put_units(self, world: World, paths_for_my_units: List[Path]):
        """
        """
        hand, myself = self.choose_units(world)
        # multi path
        if len(paths_for_my_units) > 1:
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
            # reversed best are in the end
            for unit in reversed(hand):
                if unit.ap <= myself.ap:
                    myself.ap -= unit.ap
                    Logs.show_log(
                        f"unit: {unit.type_id} in path: {paths_for_my_units[0].id}")
                    world.put_unit(base_unit=unit, path=paths_for_my_units[0])

    def friend_in_danger(self, world: World) -> Path:
        """
        """
        paths = world.get_friend().paths_from_player
        if world.get_friend().king.target_cell:
            target_cell = world.get_friend().king.target_cell
            for path in paths:
                if target_cell in path.cells:
                    return path
        else:
            enemy_units = world.get_first_enemy().units
            enemy_units.extend(world.get_second_enemy().units)
            for path in paths:
                # units in cell 8 => king.range+2
                # to be perepared
                cell_units = world.get_cell_units(path.cells[7])
                cell_units.extend(world.get_cell_units(path.cells[6]))
                if any(unit in cell_units for unit in enemy_units):
                    return path
        return None

    def allied_mode(self, world: World):
        """
        """
        target_path = self.friend_in_danger(world)
        return [target_path]

    def in_danger(self, world: World) -> Path:
        """
        """
        paths = world.get_me().paths_from_player
        if world.get_me().king.target_cell:
            target_cell = world.get_me().king.target_cell
            for path in paths:
                if target_cell in path.cells:
                    return path
        else:
            enemy_units = world.get_first_enemy().units
            enemy_units.extend(world.get_second_enemy().units)
            for path in paths:
                # units in cell 8 => king.range+2
                # to be perepared
                cell_units = world.get_cell_units(path.cells[8])
                cell_units.extend(world.get_cell_units(path.cells[7]))
                cell_units.extend(world.get_cell_units(path.cells[6]))
                if any(unit in cell_units for unit in enemy_units):
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

    def fucked_up(self, world: World):
        """
        """
        return not world.get_friend().is_alive()

    def delta_mode(self, world: World):
        """
        """
        paths = []
        paths.append(world.get_friend().paths_from_player[0])
        my_path = self.in_danger(world)
        if my_path:
            paths.append(my_path)
        return paths
