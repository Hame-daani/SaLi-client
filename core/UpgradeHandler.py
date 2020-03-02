from typing import List

from model import Logs, Path,Cell
from world import World


class UpgradeHandler:
    def __init__(self):
        super().__init__()
    def Manhatan_Distance(self, BeginingCell: Cell, EndingCell: Cell) -> int:
        """
        این تابع فاصله منهتنی یک سلول نسبت به یک سلول دیگر را برمیگردانذ
        """
        import math
        dist =int( math.fabs(BeginingCell.row-EndingCell.row) +
            math.fabs(BeginingCell.col-EndingCell.col))
        return dist
    def process(self, world: World):
        """
        """
        # this code tries to upgrade damage of first unit. in case there's no damage token, it tries to upgrade range
        myself = world.get_me()
        my_units=myself.units
        Grade_Upgrade = 0
        unit = None
        if world.get_range_upgrade_number is not 0 or world.get_damage_upgrade_number is not 0:
            Logs.show_log(f"have upgrade.")
            Logs.show_log(f"range :{world.get_range_upgrade_number()}")
            Logs.show_log(f"damage :{world.get_damage_upgrade_number()}")

        if len(my_units) > 0:
            for _unit in my_units:
               if(_unit.range>1):
                    temp_grade = _unit.hp + _unit.attack+_unit.range
                    if (temp_grade > Grade_Upgrade):
                         Grade_Upgrade = temp_grade
                         unit = _unit
            if(unit is not None):
               Logs.show_log(f"my  unit :{unit}")
               world.upgrade_unit_range(unit=unit)
               world.upgrade_unit_damage(unit=unit)
               Logs.show_log(f"my unit upgrade-> damage level:{unit.damage_level}  range :{unit.range_level}")



