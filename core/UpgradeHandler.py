from typing import List

from model import Logs, Path,Cell,Unit,Player
from world import World


class UpgradeHandler:
    def __init__(self,paths_for_my_units: List[Path]):
        super().__init__()
        self.paths_for_my_units = paths_for_my_units
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

          if len(my_units) > 0:
              for _unit in my_units:
                 if(_unit.base_unit.type_id == 0 or _unit.base_unit.type_id==6):
                      Logs.show_log(f"UPGRADE -> Unit;{_unit} -> dist :{self.near(world, _unit)}")
                      temp_grade = _unit.hp + _unit.attack*2+_unit.range*3
                      if (temp_grade > Grade_Upgrade and self.near(world,_unit)>4):
                           Grade_Upgrade = temp_grade
                           unit = _unit
              if(unit is not None):
                    Logs.show_log(f"my  unit :{unit}")
                    world.upgrade_unit_range(unit=unit)
                    world.upgrade_unit_damage(unit=unit)
                    Logs.show_log(f"my unit upgrade-> damage level:{unit.damage_level} range :{unit.range_level} (0_0) "
                                  f"dist:{self.near(world,unit)}")
