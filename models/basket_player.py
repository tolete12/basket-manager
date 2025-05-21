import sqlite3
from dataclasses import dataclass
from models.player import Player


@dataclass
class BasketPlayer(Player):
    # BASKETBALL
    layup = 0
    dunk = 0
    close_shooting = 0
    mid_range_shooting = 0
    three_shooting = 0
    corner_shooting = 0
    free_throw = 0
    passing = 0
    off_the_ball = 0
    low_post = 0
    high_post = 0
    def_rebounding = 0
    off_rebounding = 0
    stealing = 0
    ball_defence = 0
    off_ball_defence = 0
    screening = 0
    changing_screens = 0
    handling = 0
    blocking = 0

    def __init__(self, row: sqlite3.Row):
        super().__init__(row)
    
    @classmethod    
    def from_dict(cls, data: dict[str, str]) -> "BasketPlayer":
        return cls(**data)
