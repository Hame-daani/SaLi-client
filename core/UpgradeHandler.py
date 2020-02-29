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
        if world.get_range_upgrade_number or world.get_damage_upgrade_number:
            Logs.show_log(f"have upgrade.")
        if len(my_units) > 0:

            for _unit in my_units:
              temp_grade = _unit.hp + _unit.damage_level
              if (temp_grade > Grade_Upgrade):
                  Grade_Upgrade = temp_grade
                  unit = _unit
            world.upgrade_unit_damage(unit=unit)
            world.upgrade_unit_range(unit=unit)


