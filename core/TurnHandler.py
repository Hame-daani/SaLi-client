import random
from typing import List

from core.PickHandler import PickHandler
from model import Path, Logs, Spell, SpellTarget
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
        if myself.ap >= max_ap//2:
            for base_unit in myself.hand:
                world.put_unit(base_unit=base_unit, path=path_for_my_units)

# اسپل ها
# دو نوع اسپل داریم
# اسپل محیطی و اسپل یونیتی
# اسپل های محیطی با توجه ب نوعشون باید در بهترین مکان زده بشن مثلا اسپل محیطی سم ک برای دشمن زده میشه باید در مکانی زده بشه ک بیشترین دشمن در اونجا قرار داره
# و بقیه اسپل ها هم همینطور

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
        if received_spell.target == SpellTarget.ENEMY:
            enemy_units = world.get_first_enemy().units
            enemy_units.extend(world.get_second_enemy().units)
            if len(enemy_units) > 0:
                world.cast_area_spell(
                    center=enemy_units[0].cell, spell=received_spell)
        elif received_spell.target == SpellTarget.ALLIED:
            friend_units = world.get_friend().units
            if len(friend_units) > 0:
                world.cast_area_spell(
                    center=friend_units[0].cell, spell=received_spell)
        elif received_spell.target == SpellTarget.SELF:
            myself = world.get_me()
            my_units = myself.units
            if len(my_units) > 0:
                world.cast_area_spell(
                    center=my_units[0].cell, spell=received_spell)

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
