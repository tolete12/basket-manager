import random

from db.createrecords.calendars.create_calendars import CreateCalendars
from db.sql_lite_helper import SQLLiteHelper


class CreateNBACalendar(CreateCalendars):

    def __init__(self, sql_helper: SQLLiteHelper, stadiums_info: dict, translations: dict, season_info: dict = None,
                 calendar_id: int = None):
        super().__init__(sql_helper, stadiums_info, translations, season_info, calendar_id)

    def create_nba_calendar(self):
        nba_league_id = self.sql_helper.get_league_id_by_abrev('NBA')
        self.nba_same_division(
            self.sql_helper.get_div_with_teams_hierarchy(str(nba_league_id), 'DIVISIONS.DIVISION_ID'), nba_league_id)
        self.nba_same_conference_different_division(
            self.sql_helper.get_div_conf_with_teams_hierarchy(str(nba_league_id)), nba_league_id)
        self.nba_different_conference(
            self.sql_helper.get_div_with_teams_hierarchy(str(nba_league_id), 'CONFERENCES.CONFERENCE_ID'),
            nba_league_id)

    def nba_same_division(self, div_and_teams: dict, nba_league_id):
        [self.nba_add_games_same_division(div_and_teams[division], nba_league_id) for division in div_and_teams]

    def nba_add_games_same_division(self, teams: list, nba_league_id):
        for visitor_team in teams:
            for local_team in teams:
                if visitor_team == local_team:
                    continue
                self.add_games(local_team, visitor_team, nba_league_id, True)
                self.add_games(local_team, visitor_team, nba_league_id, True)

    def nba_add_games_same_conference_different_division(self, rivals_list_four: list, team_id: int, rand: int,
                                                         rival_teams_ids: list, rival_teams: dict, nba_league_id):
        for team_rival_id in rivals_list_four:
            self.add_games(team_rival_id, team_id, nba_league_id, True)
            self.add_games(team_rival_id, team_id, nba_league_id, True)
            self.add_games(team_id, team_rival_id, nba_league_id, True)
            self.add_games(team_id, team_rival_id, nba_league_id, True)

        index = 1

        remaining_teams = self.nba_same_conference_different_division_remaining_teams(
            rival_teams_ids, rivals_list_four, rand)

        rand += 1
        if rand > len(rival_teams_ids):
            rand = 1
        for team_rival_id in remaining_teams:
            if rival_teams[team_rival_id] == 1:
                self.add_games(team_rival_id, team_id, nba_league_id, True)
                self.add_games(team_rival_id, team_id, nba_league_id, True)
                self.add_games(team_id, team_rival_id, nba_league_id, True)
                continue
            if index == 1:
                index += 1
                rival_teams[team_rival_id] += 1
                self.add_games(team_rival_id, team_id, nba_league_id, True)
                self.add_games(team_id, team_rival_id, nba_league_id, True)
                self.add_games(team_id, team_rival_id, nba_league_id, True)
            else:
                self.add_games(team_rival_id, team_id, nba_league_id, True)
                self.add_games(team_rival_id, team_id, nba_league_id, True)
                self.add_games(team_id, team_rival_id, nba_league_id, True)
        return rand

    def nba_define_games_same_conference_different_division(self, rival_teams_ids: list, team_id: int,
                                                            rival_teams: dict, rand: int, nba_league_id):
        rivals_list_four = []
        rand_temp = rand
        while len(rivals_list_four) < 3:
            rivals_list_four.append(rival_teams_ids[rand_temp - 1])
            rand_temp += 1
            if rand_temp > len(rival_teams_ids):
                rand_temp = 1
        rand = self.nba_add_games_same_conference_different_division(rivals_list_four, team_id, rand,
                                                                     rival_teams_ids, rival_teams, nba_league_id)
        return rand

    def nba_same_conference_different_division(self, confs_divs_teams: dict, nba_league_id):
        for conference_id in confs_divs_teams:
            for division_id_1 in confs_divs_teams[conference_id]:
                for division_id_2 in confs_divs_teams[conference_id]:
                    if division_id_2 > division_id_1:
                        division_teams = confs_divs_teams[conference_id][division_id_1]
                        rival_teams = dict(zip(confs_divs_teams[conference_id][division_id_2],
                                               [0] * len(confs_divs_teams[conference_id][division_id_2])))
                        rival_teams_ids = list(rival_teams.keys())
                        rand = random.randint(1, len(rival_teams_ids))
                        for team_id in division_teams:
                            rand = self.nba_define_games_same_conference_different_division(rival_teams_ids, team_id,
                                                                                            rival_teams, rand,
                                                                                            nba_league_id)

    @staticmethod
    def nba_same_conference_different_division_remaining_teams(rival_teams_ids: list, rivals_list_four: list,
                                                               rand: int):
        remaining_teams = []
        rand_temp_2 = rand

        for i in range(rand_temp_2, len(rival_teams_ids) + 1):
            if rival_teams_ids[i - 1] not in rivals_list_four:
                remaining_teams.append(rival_teams_ids[i - 1])
            if i == len(rival_teams_ids):
                for j in range(1, rand_temp_2 + 1):
                    if rival_teams_ids[j - 1] not in rivals_list_four:
                        remaining_teams.append(rival_teams_ids[j - 1])
        return remaining_teams

    def nba_different_conference(self, conf_and_teams, league_id):
        self.generic_add_games_different_conference(conf_and_teams, league_id)
