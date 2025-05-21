from db.sql_lite_handler import SQLiteHandler
from db.sql_lite_helper import SQLLiteHelper
from variables.constants import PLAYER_ID, PLAYERS
from db.createrecords.players.create_players import CreatePlayers

class CreateBasketPlayers:
    def __init__(self, db_obj: SQLiteHandler, sql_helper: SQLLiteHelper):
        self.db_obj = db_obj
        self.sql_helper = sql_helper

    def number_player(self, team_id):
        return 10

    def create_players(self, team_id: int, league_id: int, level: int):
        names_dict = self.sql_helper.get_all_names()
        surnames_dict = self.sql_helper.get_all_surnames()
        # player_id = self.sql_helper.get_max_id(PLAYER_ID, PLAYERS)
        number_players = self.number_player(team_id)
        for _ in range(number_players):
            name_id, _ = CreatePlayers.get_random_from_dict(names_dict)
            suname_id, _ = CreatePlayers.get_random_from_dict(surnames_dict)
            player_dict = {
                'name_id': name_id,
                'surname_id': suname_id,
                'birthdate_id': 0,
                'team_id': team_id,
                'height': 0,
                'weight': 0,
                'intelligence': 0,
                'positioning': 0,
                'temperament': 0,
                'leadership': 0,
                'team_player': 0,
                'aggression': 0,
                'potential': 0,
                'mental_toughness': 0,
                'health': 0,
                'tactics': 0,
                'speed': 0,
                'acceleration': 0,
                'natural_fitness': 0,
                'stamina': 0,
                'jumping': 0,
                'strength': 0,
                'balance': 0,
                'side_scrolling': 0,
                'dribbling': 0,
                'layup': 0,
                'dunk': 0,
                'close_shooting': 0,
                'mid_range_shooting': 0,
                'three_shooting': 0,
                'corner_shooting': 0,
                'free_throw': 0,
                'passing': 0,
                'off_the_ball': 0,
                'low_post': 0,
                'high_post': 0,
                'def_rebounding': 0,
                'off_rebounding': 0,
                'stealing': 0,
                'ball_defence': 0,
                'off_ball_defence': 0,
                'screening': 0,
                'changing_screens': 0,
                'handling': 0,
                'blocking': 0
            }
