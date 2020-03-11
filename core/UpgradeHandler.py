from typing import List

from model import Logs, Path,Cell,Unit,Player
from world import World


class UpgradeHandler:
    def __init__(self,paths_for_my_units: List[Path], special_unit:Unit):
        super().__init__()
        self.paths_for_my_units = paths_for_my_units
        self.special_unit = special_unit
    def Targeted_enemy(self, world: World) -> Player:
        My_First_Enemy = world.get_first_enemy()
        My_Second_Enemy = world.get_second_enemy()
        for path in self.paths_for_my_units:
            if My_First_Enemy.king.center in path.cells:
                return My_First_Enemy
            if My_Second_Enemy.king.center in path.cells:
                return My_Second_Enemy
    def Manhatan_Distance(self, BeginingCell: Cell, EndingCell: Cell) -> int:
        """
        این تابع فاصله منهتنی یک سلول نسبت به یک سلول دیگر را برمیگردانذ
        """
        import math
        dist =int( math.fabs(BeginingCell.row-EndingCell.row) +
            math.fabs(BeginingCell.col-EndingCell.col))
        return dist
    def enemt_level_Logs(self,world:World):
        enemy_unit=world.get_first_enemy().units
        enemy_unit.extend(world.get_second_enemy().units)
        Logs.show_log(f"///--------------------------ME-----------------------------------////")
        for _unit in world.get_me().units:
            if(_unit.range_level>0):
                Logs.show_log(f"unit->id :{_unit.unit_id}  player id :{_unit.player_id}"
                              f"  damage level :{_unit.damage_level}  range level :{_unit.range_level}"
                              f"  unit->attack :{_unit.attack} unit->hp :{_unit.hp}"
                              f"  base unit id :{_unit.base_unit.type_id}"
                              f"  unit cell : {_unit.cell}")
        Logs.show_log(f"///-------------------------------------------------------------////")
        Logs.show_log(f"///------------------------Enemy-------------------------------------////")
        for unit in enemy_unit:
            if(unit.range_level>0 or unit.damage_level>0):
                Logs.show_log(f"unit->id :{unit.unit_id}  player id :{unit.player_id}"
                              f"  damage level :{unit.damage_level}  range level :{unit.range_level}"
                              f"  unit->attack :{unit.attack} unit->hp :{unit.hp}"
                              f"  base unit id :{unit.base_unit.type_id}"
                              f"  unit cell : {unit.cell}")
        Logs.show_log(f"///-------------------------------------------------------------////")

    def near(self,world:World,unit:Unit)->int:
        my_enemy = self.Targeted_enemy(world)
        my_enemy_units = my_enemy.units
        dist=10000
        for enemy in my_enemy_units:
            temp=self.Manhatan_Distance(enemy.cell,unit.cell)
            if(temp<=dist):
                dist=temp
        return  dist

    def process(self, world: World):
        """
        """
        self.enemt_level_Logs(world)
        # this code tries to upgrade damage of first unit. in case there's no damage token, it tries to upgrade range
        myself = world.get_me()
        my_units=myself.units
        my_enemy=self.Targeted_enemy(world)
        my_enemy_units=my_enemy.units

        Grade_Upgrade = 0
        unit = None

        if world.get_range_upgrade_number() is not 0 or world.get_damage_upgrade_number() is not 0:
          Logs.show_log(f"have upgrade.")
          Logs.show_log(f"range :{world.get_range_upgrade_number()}")
          Logs.show_log(f"damage :{world.get_damage_upgrade_number()}")

          for unit in myself.units:
              if (unit.base_unit.type_id == 0):
                  if (self.Manhatan_Distance(unit.cell, myself.king.center) <= 2 or unit.range_level > 0):
                      if (world.get_range_upgrade_number() > 2 or unit.range_level > 0):
                          world.upgrade_unit_range(unit=unit)
                          if (world.get_range_upgrade_number() == 0):
                              world.upgrade_unit_damage(unit=unit)
                          Logs.show_log(f"my upgrade unit : {unit} -> Range Level:{unit.range_level}"
                                        f"   Damege Level : {unit.damage_level}"
                                        f"   unit cell : {unit.cell}")