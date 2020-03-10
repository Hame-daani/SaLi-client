import random
from typing import List

from model import Cell, Logs, Path, Spell, SpellTarget, SpellType, Unit, Player
from world import World


class SpellHandler:
    def __init__(self, paths_for_my_units: List[Path],splls: List[Spell]):
        super().__init__()
        self.paths_for_my_units = paths_for_my_units
        self._splls_=splls
        self.targeted_enemy:Player=None
    def Targeted_enemy(self,world:World)->Player:
        My_First_Enemy = world.get_first_enemy()
        My_Second_Enemy = world.get_second_enemy()
        for path in self.paths_for_my_units:
            if My_First_Enemy.king.center in path.cells:
                return My_First_Enemy
            if My_Second_Enemy.king.center in path.cells:
                return My_Second_Enemy
    def process(self, world: World)-> Spell:
        """
        """
        # this code tries to cast the received spell
        self.targeted_enemy=self.Targeted_enemy(world)
        received_spell = world.get_received_spell()
        if received_spell is not None:
            Logs.show_log(f"spell {received_spell.type} cast.")
            if received_spell.is_area_spell():
              received_spell =  self.put_area_spell(received_spell, world)
            else:  # if is unit spell
              received_spell =  self.put_unit_spell(world,received_spell)
        for spell in self._splls_:
            Logs.show_log(f" 0(*_._*)0 Spell list 0(*_._*)0 :{spell}")
            cast_spell = spell
            Logs.show_log(f"spell {cast_spell.type} cast.")
            if cast_spell.is_area_spell():
                cast_spell = self.put_area_spell(cast_spell, world)
            else:  # if is unit spell
                cast_spell = self.put_unit_spell(world, cast_spell)
            if(cast_spell is None):
                self._splls_.remove(spell)
        Logs.show_log(f" Fuck Received : {received_spell}")
        return received_spell

    def Check_Enemy_or_familiar_Unit(self, world: World, unit: Unit, enemy_familiar: bool) -> bool:
        """
        این نابع چک میکند که یونیت داده شده جز آن دسته خواسته شده است یا نه
        enemy = false
        familiar= true
        """
        # -----------------------------
        My_Player = world.get_me()
        My_First_Enemy = world.get_first_enemy()
        My_Second_Enemy = world.get_second_enemy()
        My_Freind = world.get_friend()
        # ------------------------------
        All_units_own = My_Player.units
        All_units_enemy = My_First_Enemy.units

        for unit in My_Freind.units:
            All_units_own.append(unit)
        for unit in My_Second_Enemy.units:
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

    def Manhatan_Distance(self, BeginingCell: Cell, EndingCell: Cell) -> int:
        """
        این تابع فاصله منهتنی یک سلول نسبت به یک سلول دیگر را برمیگردانذ
        """
        import math
        dist_row =math.fabs(BeginingCell.row-EndingCell.row)
        dist_cul=math.fabs(BeginingCell.col-EndingCell.col)
        dist=dist_cul+dist_row
        return int(dist)

    def Check_Unit_Number_in_Manhatan(self, world: World, Center: Cell, distance: int
                                      , enemy_familiar: bool) -> List["Path"]:
        """
        این تابع باید چک کند در فاصله
        k 
        از یک خانه یونیتی وجود دارد
        """
        All_path_in_map = world.get_map().paths
        All_path_have_Center_Cell = []
        Enemy_in_path=[]
        for path in All_path_in_map:
            if(path.cells.__contains__(Center)):
                All_path_have_Center_Cell.append(path)
        for path in All_path_have_Center_Cell:
            Number_unit = 0
            for cell in path.cells:
                if(self.Manhatan_Distance(Center, cell) <= distance):
                    for unit in world.get_cell_units(cell=cell):
                        if(self.Check_Enemy_or_familiar_Unit(world, unit, enemy_familiar) == True):
                            Number_unit = Number_unit+1
            if(Number_unit>0):
                Enemy_in_path.append(path)
                break
        return Enemy_in_path

    # استراتیزی...
    # مسیر ها
    # ۱-مسیر انتخابی اولیه مسیر مستقیم به یکی از حریف ها باشه
    # معمولا در بازی دو مسیر به دشمنا هست یکی مسیر مستقیم از تو به یکی از دشمنا و دیگری مسیرمستقیم از یارت به حریف مستقیم یارت
    # ۲-اگر دشمن مستقیم از بین رفت مسیر انتخابی تغییر پیدا میکند به مسیر یار البته باید تست شود ک مسیر ب وجود اماده اولیه بعد از شکست حریف اولی بهتر است یا مسیر مستقیم ب سمت یار
    # ۳-اگر یاز ما خیلی کصخول بود و سریعا از بین رفت ممکن است از چند مسیر به ما حمله شود پس بهتر است در هردو مسیری ک ب ما ختم میشود نیرو بفرستیم برای مقابله با هردو دشمن


# اسپل ها
# دو نوع اسپل داریم
# اسپل محیطی و اسپل یونیتی
# اسپل های محیطی با توجه ب نوعشون باید در بهترین مکان زده بشن مثلا اسپل محیطی سم ک برای دشمن زده میشه باید در مکانی زده بشه ک بیشترین دشمن در اونجا قرار داره
# و بقیه اسپل ها هم همینطور

    def Grade_Hp_Enemy_Cell(self, units:List["Unit"]) -> int:
        grad = 0
        for unit in units:
            if(unit.hp < 10):
                grad = grad+4
            elif(unit.hp < 15):
                grad = grad+2
            else:
                grad = grad+1
        return grad
    def Grade_Hp_Allied_Cell(self, units:List["Unit"]) -> int:
        grad = 0
        for unit in units:
            hp = unit.base_unit.max_hp - unit.hp
            if(unit.hp>3 and hp>3):
                 if(hp <=5):
                     grad = grad+1
                 elif(hp <= 10):
                     grad = grad+2
                 elif(hp <= 20):
                     grad = grad +4
        return grad
    def BestCell(self, world: World, received_spell: Spell):
        # -----------------------------
        My_Player = world.get_me()
        My_First_Enemy = self.Targeted_enemy(world)
        #My_Second_Enemy = world.get_second_enemy()
        #My_Freind = world.get_friend()
        # ------------------------------

        All_units_own = My_Player.units
        All_units_enemy = My_First_Enemy.units
        #all unit ->path unit
        """for unit in My_Freind.units:
            All_units_own.append(unit)
        for unit in My_Second_Enemy.units:
            All_units_enemy.append(unit)"""
        # --------------------------------
        Select_Cell = None

        if(received_spell.target == SpellTarget.ENEMY):
            num_enemy_around_cell = 3
            grade_cell = 5
            Targets=[]
            Logs.show_log(f"target enemy -> spell type : {received_spell.type}")
            #best cell for HP(Posion And Damage)
            for unit in self.paths_for_my_units[0].cells:

                target = world.get_area_spell_targets(
                    center=unit, spell=received_spell)
                grade_cell_temp = self.Grade_Hp_Enemy_Cell(target)
                Logs.show_log(f"Grade:{grade_cell_temp} -- Unit num :{len(target)}")
                if(len(target) >= num_enemy_around_cell and grade_cell_temp >= grade_cell):
                    Logs.show_log(f"Grade:{grade_cell_temp} -- Unit:{unit}")
                    num_enemy_around_cell = len(target)
                    grade_cell = grade_cell_temp
                    Select_Cell = unit
                    Targets=target
            Logs.show_log(f"Target cell :{Select_Cell}")
            for uni in Targets:
                Logs.show_log((f" enemy unit : {uni}  hp:{uni.hp}"))

        elif(received_spell.target == SpellTarget.ALLIED):
            Logs.show_log(f"target Allied -> spell type : {received_spell.type}")
            Targets=[]
            if(received_spell.type == SpellType.HP):
                num_enemy_around_cell = 3
                grade_cell = 4
                for unit in self.paths_for_my_units[0].cells:
                    target = world.get_area_spell_targets(
                        center=unit, spell=received_spell)
                    grade_cell_temp = self.Grade_Hp_Allied_Cell(target)
                    Logs.show_log(f" hp -> {grade_cell_temp} - > num unit : {len(target)}")
                    if (len(target) >= num_enemy_around_cell and grade_cell_temp > grade_cell):
                        Logs.show_log(f"Grade:{grade_cell_temp}  --  Unit:{unit}")
                        num_enemy_around_cell = len(target)
                        Targets=target
                        grade_cell = grade_cell_temp
                        Select_Cell = unit
            elif(received_spell.type == SpellType.DUPLICATE):
                # cell for Haste And Duolicate
                num_enemy_around_cell = 3
                distance_unit_to_select_enemy=1000000

                for unit in self.paths_for_my_units[0].cells:
                    target = world.get_area_spell_targets(
                        center=unit, spell=received_spell)
                    targeted_cell_enemy=self.Manhatan_Distance(unit,self.targeted_enemy.king.center)
                    Logs.show_log(f" DUPLICATE Number arround : {len(target)} "
                                  f" -- dist to enemy :{targeted_cell_enemy}")
                    if (len(target) >= num_enemy_around_cell and targeted_cell_enemy<distance_unit_to_select_enemy ):
                        Logs.show_log(f" Number arround : {len(target)}  --  Unit :{unit}"
                                      f" -- dist to enemy :{targeted_cell_enemy}")
                        distance_unit_to_select_enemy=targeted_cell_enemy
                        num_enemy_around_cell = len(target)
                        Targets=target
                        Select_Cell = unit
            else:
                num_enemy_around_cell = 2

                for unit in self.paths_for_my_units[0].cells:
                    target = world.get_area_spell_targets(
                        center=unit, spell=received_spell)
                    if (len(target) > num_enemy_around_cell ):
                        Logs.show_log(
                            f" Number arround : {len(target)}  --  Unit :{unit} ")
                        num_enemy_around_cell = len(target)
                        Select_Cell = unit
                        Targets = target

            Logs.show_log(f"target alied best select  :{Select_Cell}")
            for uni in Targets:
                Logs.show_log((f" my unit : {uni}  hp:{uni.hp}"))

        return Select_Cell

    def put_area_spell(self, received_spell: Spell, world: World)->Spell:
        """
        """
        Target_Cell = self.BestCell(world, received_spell)
        if(Target_Cell is not None):
            world.cast_area_spell(center=Target_Cell, spell=received_spell)
            received_spell=None
        return received_spell

    def put_unit_spell(self, world: World, received_spell: Spell)->Spell:
        """
        """
        myself = world.get_me()
        my_units = myself.units
        Grade_tele=0
        if len(my_units) > 0:
            unit = None
            for _unit in my_units:
                if(self.Manhatan_Distance(BeginingCell=myself.king.center,EndingCell=_unit.cell)<=3):
                    temp_grade=_unit.hp+_unit.damage_level
                    if(temp_grade>Grade_tele and _unit.hp>0):
                        Grade_tele=temp_grade
                        unit=_unit

            my_paths = self.paths_for_my_units
            path = my_paths[random.randint(0, len(my_paths) - 1)]
            size = len(path.cells)
            cell = path.cells[int((size - 1) / 2)]
            Logs.show_log(f"target Self -> spell type : {received_spell.type}")
            Logs.show_log(f"unit : {unit}  unit cell : {unit.cell}  cell : {cell}")
            world.cast_unit_spell(
                unit=unit, path=path, cell=cell, spell=received_spell)
            received_spell=None
        return received_spell
