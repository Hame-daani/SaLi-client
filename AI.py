import random

from model import *
from world import World
import time
from typing import *
from core import PickHandler, TurnHandler


class AI:
    def __init__(self):
        self.rows = 0
        self.cols = 0
        self.path_for_my_units: List[Path] = None
    # this function is called in the beginning for deck picking and pre process

    def pick(self, world: World):
        start_time = time.time()
        Logs.show_log("pick started!")
        PickHandler.pick(self, world)
        Logs.show_log(f"pick finished! time:{time.time()-start_time}")
    # it is called every turn for doing process during the game

    def turn(self, world: World):
        start_time = time.time()
        Logs.show_log(f"turn {world.get_current_turn()} started.")
        TurnHandler.turn(self, world)
        Logs.show_log(
            f"turn {world.get_current_turn()} finished. time: {time.time()-start_time}")
    # it is called after the game ended and it does not affect the game.
    # using this function you can access the result of the game.
    # scores is a map from int to int which the key is player_id and value is player_score

    def end(self, world: World, scores):
        print("end started!")
        print("My score:", scores[world.get_me().player_id])
