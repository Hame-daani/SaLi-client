import random
from typing import List

from core.PickHandler import PickHandler
from model import Cell, Logs, Path, Spell, SpellTarget, SpellType, Unit
from world import World


class TurnHandler:
    """
    """

    def __init__(self, pick_handler: PickHandler):
        super().__init__()
        self.pick_handler = pick_handler

    def turn(self, world: World):
        """
        """
        # Process Unit Puting
        self.unit_process(world)
        # Process Spell Puting
        self.spell_process(world)
        # Process Upgrades
        self.upgrade_process(world)

    # enemy = false familiar= true
    # این نابع چک میکند که یونیت داده شده جز آن دسته خواسته شده است یا نه
    def Check_Enemy_or_familiar_Unit(self, world: World, unit: Unit, enemy_familiar: bool) -> bool:
        # -----------------------------
        self.My_Player = world.get_me()
        self.My_First_Enemy = world.get_first_enemy()
        self.My_Second_Enemy = world.get_second_enemy()
        self.My_Freind = world.get_friend()
        # ------------------------------
        All_units_own = self.My_Player.units
        All_units_enemy = self.My_First_Enemy.units

        for unit in self.My_Freind.units:
            All_units_own.append(unit)
        for unit in self.My_Second_Enemy.units:
            All_units_enemy.append(unit)
        # --------------------------------
        if(enemy_familiar == False):
            if(All_units_enemy.__contains__(unit)):
                return True
            else:
                return False
        else:
            if(All_units_own.__contains__(unit)):
                return True
            else:
                return False
    # این تابع فاصله منهتنی یک سلول نسبت به یک سلول دیگر را برمیگردانذ

    def Manhatan_Distance(self, BeginingCell: Cell, EndingCell: Cell) -> int:
        import math
        dist = math.fabs(BeginingCell.row-EndingCell.row) + \
            math.fabs(BeginingCell.col-EndingCell.col)
        return dist
    # این تابع باید چک کند در فاصله k از یک خانه یونیتی وجود دارد

    def Check_Unit_Number_in_Manhatan(self, world: World, Center: Cell, distance: int, enemy_familiar: bool) -> int:
        All_path_in_map = world.get_map().paths
        All_path_have_Center_Cell = []
        Number_unit = 0
        for path in All_path_in_map:
            if(path.cells.__contains__(Center)):
                All_path_have_Center_Cell.append(path)
        for path in All_path_have_Center_Cell:
            for cell in path.cells:
                if(self.Manhatan_Distance(Center, cell) <= distance):
                    for unit in world.get_cell_units(cell=cell):
                        if(self.Check_Enemy_or_familiar_Unit(world, unit, enemy_familiar) == True):
                            Number_unit = Number_unit+1
        return Number_unit

    # استراتیزی...
    # مسیر ها
    # ۱-مسیر انتخابی اولیه مسیر مستقیم به یکی از حریف ها باشه
    # معمولا در بازی دو مسیر به دشمنا هست یکی مسیر مستقیم از تو به یکی از دشمنا و دیگری مسیرمستقیم از یارت به حریف مستقیم یارت
    # ۲-اگر دشمن مستقیم از بین رفت مسیر انتخابی تغییر پیدا میکند به مسیر یار البته باید تست شود ک مسیر ب وجود اماده اولیه بعد از شکست حریف اولی بهتر است یا مسیر مستقیم ب سمت یار
    # ۳-اگر یاز ما خیلی کصخول بود و سریعا از بین رفت ممکن است از چند مسیر به ما حمله شود پس بهتر است در هردو مسیری ک ب ما ختم میشود نیرو بفرستیم برای مقابله با هردو دشمن

    def unit_process(self, world: World):
        """
        """
        path_for_my_units = self.choose_path(world)
        Logs.show_log(f"path {path_for_my_units} chosen")
        self.put_units(world, path_for_my_units)

    def choose_path(self, world: World) -> Path:
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
        # ----------------------------------
        self.path_for_my_units_ = path_for_my_units
        # ----------------------------------
        return path_for_my_units

    def put_units(self, world: World, path_for_my_units: Path):
        """
        """
        myself = world.get_me()
        max_ap = world.get_game_constants().max_ap
        # play all of hand once your ap reaches maximum. if ap runs out, putUnit doesn't do anything
        if myself.ap >= max_ap // 2:
            for base_unit in myself.hand:
                world.put_unit(base_unit=base_unit, path=path_for_my_units)

# اسپل ها
# دو نوع اسپل داریم
# اسپل محیطی و اسپل یونیتی
# اسپل های محیطی با توجه ب نوعشون باید در بهترین مکان زده بشن مثلا اسپل محیطی سم ک برای دشمن زده میشه باید در مکانی زده بشه ک بیشترین دشمن در اونجا قرار داره
# و بقیه اسپل ها هم همینطور
    def GradeCell(self, units: List["Unit"]) -> int:
        grad = 0
        for unit in units:
            if(unit.hp < 5):
                grad = grad+4
            elif(unit.hp < 10):
                grad = grad+2
            else:
                grad = grad+1
        return grad

    def BestCell(self, world: World, received_spell: Spell):
        # -----------------------------
        self.My_Player = world.get_me()
        self.My_First_Enemy = world.get_first_enemy()
        self.My_Second_Enemy = world.get_second_enemy()
        self.My_Freind = world.get_friend()
        # ------------------------------

        All_units_own = self.My_Player.units
        All_units_enemy = self.My_First_Enemy.units

        for unit in self.My_Freind.units:
            All_units_own.append(unit)
        for unit in self.My_Second_Enemy.units:
            All_units_enemy.append(unit)
        # --------------------------------
        Select_Cell = None

        if(received_spell.target == SpellTarget.ENEMY):
            num_enemy_around_cell = 0
            grade_cell = 0
            # best cell for HP(Posion And Damage)
            for unit in All_units_enemy:

                target = world.get_area_spell_targets(
                    center=unit.cell, spell=received_spell)
                grade_cell_temp = self.GradeCell(target)

                print("target : ", target.__len__(),
                      "   grade : ", grade_cell_temp)

                if(target.__len__() >= num_enemy_around_cell & grade_cell_temp >= grade_cell):
                    print("garde : ", grade_cell_temp)
                    num_enemy_around_cell = target.__len__()
                    grade_cell = grade_cell_temp
                    Select_Cell = unit.cell

            print("target enemy : ", Select_Cell)

        elif(received_spell.target == SpellTarget.ALLIED):

            if(received_spell.type == SpellType.HP):
                num_enemy_around_cell = 0
                grade_cell = 0
                for unit in All_units_own:
                    target = world.get_area_spell_targets(
                        center=unit.cell, spell=received_spell)
                    grade_cell_temp = self.GradeCell(target)
                    print("target : ", target.__len__(),
                          "   grade : ", grade_cell_temp)
                    if (target.__len__() >= num_enemy_around_cell & grade_cell_temp >= grade_cell):
                        print("grade : ", grade_cell_temp)
                        num_enemy_around_cell = target.__len__()
                        grade_cell = grade_cell_temp
                        Select_Cell = unit.cell
            else:
                # cell for Haste And Duolicate
                num_enemy_around_cell = 0
                for unit in All_units_own:
                    target = world.get_area_spell_targets(
                        center=unit.cell, spell=received_spell)
                    if (target.__len__() > num_enemy_around_cell):
                        num_enemy_around_cell = target.__len__()
                        Select_Cell = unit.cell

            print("target alied :", Select_Cell, "  nume unit : ",
                  world.get_cell_units(Select_Cell).__len__())
        print("Best Select_Cell : ", Select_Cell)
        return Select_Cell

    def spell_process(self, world: World):
        """
        """
        # this code tries to cast the received spell
        received_spell = world.get_received_spell()
        if received_spell is not None:
            Logs.show_log(f"spell {received_spell.type} cast.")
            if received_spell.is_area_spell():
                self.put_area_spell(received_spell, world)
            else:  # if is unit spell
                self.put_unit_spell(world, received_spell)

    def put_area_spell(self, received_spell: Spell, world: World):
        """
        """
        Target_Cell = self.BestCell(world, received_spell)
        world.cast_area_spell(center=Target_Cell, spell=received_spell)

    def put_unit_spell(self, world: World, received_spell: Spell):
        """
        """
        myself = world.get_me()
        my_units = myself.units
        if len(my_units) > 0:
            unit = my_units[0]
            my_paths = self.path_for_my_units_
            path = my_paths[random.randint(0, len(my_paths) - 1)]
            size = len(path.cells)
            cell = path.cells[int((size - 1) / 2)]
            world.cast_unit_spell(
                unit=unit, path=path, cell=cell, spell=received_spell)

    def upgrade_process(self, world: World):
        """
        """
        # this code tries to upgrade damage of first unit. in case there's no damage token, it tries to upgrade range
        myself = world.get_me()
        if world.get_range_upgrade_number or world.get_damage_upgrade_number:
            Logs.show_log(f"have upgrade.")
        if len(myself.units) > 0:
            unit = myself.units[0]
            world.upgrade_unit_damage(unit=unit)
            world.upgrade_unit_range(unit=unit)
