import random
from typing import List

from core.PickHandler import *
from model import *
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
        Logs.show_log(f"path {path_for_my_units.id} chosen")
        self.put_units(world, path_for_my_units)

    def choose_path(self, world: World) -> Path:
        """
        """
        path_to_enemy = []
        myself = world.get_me()
        first_enemy_king_cell = world.get_first_enemy().king.center
        path_to_first_enemy = world.get_shortest_path_to_cell(
            from_player_id=myself.player_id, cell=first_enemy_king_cell)
        path_to_enemy.append(path_to_first_enemy)
        second_enemy_king_cell = world.get_second_enemy().king.center
        path_to_second_enemy = world.get_shortest_path_to_cell(
            from_player_id=myself.player_id, cell=second_enemy_king_cell)
        path_to_enemy.append(path_to_second_enemy)
        Logs.show_log(f"path 1 {path_to_enemy[0]} path 2 {path_to_enemy[1]}")
        path_for_my_units = min(path_to_enemy, key=lambda p: len(p.cells))
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
    def GradeCell(self,units:List["Unit"]) ->int:
        grad=0
        for unit in units:
            if(unit.hp<5):
                grad=grad+4
            elif(unit.hp<10):
                grad=grad+2
            else:
                grad=grad+1
        return grad
    def BestCell(self,world:World, received_spell:Spell):
        #-----------------------------
        self.My_Player = world.get_me()
        self.My_First_Enemy = world.get_first_enemy()
        self.My_Second_Enemy = world.get_second_enemy()
        self.My_Freind = world.get_friend()
        #------------------------------

        All_units_own=self.My_Player.units
        All_units_enemy=self.My_First_Enemy.units

        for unit in self.My_Freind.units:
            All_units_own.append(unit)
        for unit in self.My_Second_Enemy.units:
            All_units_enemy.append(unit)
        #--------------------------------
        Select_Cell = None

        if(received_spell.target==SpellTarget.ENEMY):
            num_enemy_around_cell=0
            grade_cell=0
            #best cell for HP(Posion And Damage)
            for unit in All_units_enemy:

                target = world.get_area_spell_targets(center=unit.cell,spell=received_spell)
                grade_cell_temp=self.GradeCell(target)

                print("target : ",target.__len__(),"   grade : ",grade_cell_temp)

                if(target.__len__()>=num_enemy_around_cell & grade_cell_temp>=grade_cell):
                    print("garde : ",grade_cell_temp)
                    num_enemy_around_cell=target.__len__()
                    grade_cell=grade_cell_temp
                    Select_Cell=unit.cell

            print("target enemy : ",Select_Cell)

        elif(received_spell.target==SpellTarget.ALLIED):
            if(received_spell.type==SpellType.HP):
                num_enemy_around_cell = 0
                grade_cell = 0
                for unit in All_units_own:
                    target = world.get_area_spell_targets(center=unit.cell, spell=received_spell)
                    grade_cell_temp = self.GradeCell(target)
                    print("target : ", target.__len__(), "   grade : ", grade_cell_temp)
                    if (target.__len__() >= num_enemy_around_cell & grade_cell_temp >= grade_cell):
                        print("grade : ",grade_cell_temp)
                        num_enemy_around_cell = target.__len__()
                        grade_cell = grade_cell_temp
                        Select_Cell = unit.cell
            else:
                #cell for Haste And Duolicate

                num_enemy_around_cell = 0
                for unit in All_units_own:
                    target = world.get_area_spell_targets(center=unit.cell, spell=received_spell)
                    if (target.__len__() > num_enemy_around_cell):
                        num_enemy_around_cell = target.__len__()
                        Select_Cell = unit.cell

            print("target alied :", Select_Cell,"  nume unit : ",world.get_cell_units(Select_Cell).__len__())
        print("Best Select_Cell : ",Select_Cell)
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
        Target_Cell=self.BestCell(world,received_spell)
        world.cast_area_spell(center=Target_Cell,spell=received_spell)


    def put_unit_spell(self, world: World, received_spell: Spell):
        """
        """
        myself = world.get_me()
        my_units = myself.units
        if len(my_units) > 0:
            unit = my_units[0]
            my_paths = myself.paths_from_player
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
