import random

from model import *
from world import World
import time
from typing import *
from core.PickHandler import PickHandler
from core.TurnHandler import TurnHandler


class AI:
    def __init__(self):
        self.pick_handler = PickHandler()

    def pick(self, world: World):
        """
        this function is called in the beginning for deck picking and pre process
        """
        start_time = time.time()
        Logs.show_log("pick started!")
        self.pick_handler.pick(world)
        Logs.show_log(f"pick finished! time:{time.time()-start_time:.4f}")

    def turn(self, world: World):
        """
        it is called every turn for doing process during the game
        """
        start_time = time.time()
        Logs.show_log(f"turn {world.get_current_turn()} started.")
        self.turn_handler = TurnHandler(pick_handler=self.pick_handler)
        self.turn_handler.turn(world)
        Logs.show_log(
            f"turn {world.get_current_turn()} finished. time: {time.time()-start_time:.4f}")

    def end(self, world: World, scores):
        """
        it is called after the game ended and it does not affect the game.
        using this function you can access the result of the game.
        scores is a map from int to int which the key is player_id and value is player_score
        """
        print("end started!")
        my_id = world.get_me().player_id
        my_friend_id = world.get_friend().player_id
        print(
            f"My ID: {my_id} My Friend: {my_friend_id} My score:{scores[my_id]}")
