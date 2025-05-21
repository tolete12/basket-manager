import random

from db.sql_lite_helper import SQLLiteHelper
from models.season import Season
from utilities import Utilities
from variables.constants import DATE_FORMAT
from models.calendar import Calendar
import datetime
from datetime import date


class CreateCalendars:

    def __init__(self, sql_helper: SQLLiteHelper, stadiums_info: dict, translations: dict, season_info: dict = None,
                 calendar_id: int = None):
        self.sql_helper = sql_helper
        self.translations = translations
        self.stadiums_info = stadiums_info
        self.games = {}
        self.nba_games = {}
        self.scheduled_games = {}
        if season_info:
            self.season_info = season_info
        else:
            self.season_info = self.sql_helper.get_latest_seasons_info()
        if calendar_id:
            self.calendar_id = calendar_id
        else:
            self.calendar_id = self.sql_helper.get_max_calendar_id()

    def fill_dates(self, start_date: str, end_date: str):
        start_date_dated = datetime.datetime.strptime(start_date, DATE_FORMAT).date() - datetime.timedelta(days=1)
        end_date_dated = datetime.datetime.strptime(end_date, DATE_FORMAT).date() + datetime.timedelta(days=1)
        while start_date_dated <= end_date_dated:
            if start_date_dated not in self.scheduled_games:
                self.scheduled_games[start_date_dated] = []
            start_date_dated = start_date_dated + datetime.timedelta(days=1)

    def add_calendar(self, home_team_id: int, away_team_id: int, game_date: datetime, game_type_id: int,
                     season_id: int, stadium_id: int = None):
        cal = Calendar()
        self.calendar_id += 1
        cal.calendar_id = self.calendar_id
        cal.team_id_1 = home_team_id
        cal.team_id_2 = away_team_id
        cal.stadium_id = stadium_id if stadium_id else self.stadiums_info[home_team_id]
        cal.score_away = 0
        cal.score_home = 0
        cal.date_id = self.sql_helper.get_date_id_from_date(game_date.date())
        cal.game_time = Utilities.convert_datetime_to_text(game_date)
        cal.temperature = 0
        cal.weather_id = 0
        cal.game_type_id = game_type_id
        cal.season_id = season_id
        if not game_date.date() in self.scheduled_games:
            self.scheduled_games[game_date.date()] = []
        self.scheduled_games[game_date.date()].append(cal)

    def is_any_game_in_stadium(self, stadium_id: int, selected_date: date):
        if list(filter(lambda x: x.stadium_id == stadium_id, self.scheduled_games[selected_date])):
            return True
        return False

    def is_allowed_by_single_date(self, home_team_id: int, away_team_id: int, selected_date: date, season_info: Season, matches: int):
        day = datetime.timedelta(days=1)
        all_star_start = Utilities.convert_text_to_date(season_info.all_star_start_date_id) - day
        all_star_end = Utilities.convert_text_to_date(season_info.all_star_end_date_id) + day
        for i in range(0, matches):
            if list(filter(lambda x: (
                        home_team_id in [x.team_id_1, x.team_id_2] or away_team_id in [x.team_id_1,
                                                                                       x.team_id_2]),
                            self.scheduled_games[selected_date + (day*i)])) or all_star_start <= selected_date + (day*i) <= all_star_end:
                return False
        return True

    def is_allowed_by_dates(self, home_team_id: int, away_team_id: int, selected_date: date, season_info: Season):

        day = datetime.timedelta(days=1)

        all_star_start = Utilities.convert_text_to_date(season_info.all_star_start_date_id) - day
        all_star_end = Utilities.convert_text_to_date(season_info.all_star_end_date_id) + day

        if (selected_date in self.scheduled_games and selected_date - day in self.scheduled_games and (
                list(filter(lambda x: (
                        home_team_id in [x.team_id_1, x.team_id_2] or away_team_id in [x.team_id_1,
                                                                                       x.team_id_2]),
                            self.scheduled_games[selected_date]))
                or list(filter(lambda x: (
                home_team_id in [x.team_id_1, x.team_id_2] or away_team_id in [x.team_id_1,
                                                                               x.team_id_2]),
                               self.scheduled_games[selected_date - day]))
        )) or (all_star_start <= selected_date <= all_star_end):
            return False
        return True

    @staticmethod
    def get_num_week_thanksgiving(nba_season_info: Season):
        # Finding thanksgiving date
        start_date_dated = datetime.datetime.strptime(nba_season_info.start_date_season, DATE_FORMAT).date()
        year = start_date_dated.year
        last_nov_day = datetime.datetime.strptime(str(year) + "-11-30", DATE_FORMAT).date()
        found = False
        while not found:
            if last_nov_day.weekday() == 3:
                found = True
            else:
                last_nov_day = last_nov_day - datetime.timedelta(days=1)

        # Finding # of week for thanksgiving
        found = False
        week_number = 1
        while not found:
            if start_date_dated == last_nov_day:
                found = True
            else:
                start_date_dated = start_date_dated + datetime.timedelta(days=7)
                week_number += 1

        return week_number

    @staticmethod
    def assign_match_to_week(home_team_id: int, away_team_id: int, teams_in_week: list, game_in_weeks: dict, week: int):
        teams_in_week.append(home_team_id)
        teams_in_week.append(away_team_id)
        game_in_weeks[week].append(tuple([home_team_id, away_team_id]))
        game_in_weeks[week].append(tuple([home_team_id, away_team_id]))
        return teams_in_week, game_in_weeks

    def add_games(self, home_team, visitor_team, league_id, append: bool):
        if league_id not in self.games:
            self.games[league_id] = {}
        if home_team not in self.games[league_id]:
            self.games[league_id][home_team] = []
        if append:
            self.games[league_id][home_team].append(visitor_team)
        else:
            self.games[league_id][home_team].extend(visitor_team)

    def generic_add_games_different_conference(self, conf_and_teams: dict, league_id):
        for conference_id_visitor, team_ids_visitor in conf_and_teams.items():
            for conference_id_local, team_ids_local in conf_and_teams.items():
                if conference_id_visitor == conference_id_local:
                    continue
                [self.add_games(team_id, team_ids_visitor, league_id, False) for team_id in team_ids_local]

    def generic_preseason_assign(self, start_date_dated: datetime.date, days_for_game: int, teams_1: list, teams_2: list,
                                 season_id: int, index: int):
        assigned = False
        while not assigned:
            selected_date = start_date_dated + datetime.timedelta(days=random.randint(0, days_for_game - 1))
            home_team = teams_1[index - 1] if index % 2 == 0 else teams_2[index - 1]
            away_team = teams_2[index - 1] if index % 2 == 0 else teams_1[index - 1]
            stadium_id = self.stadiums_info[home_team]
            if not self.is_any_game_in_stadium(stadium_id, selected_date):
                assigned = True
                game_date = datetime.datetime(selected_date.year, selected_date.month, selected_date.day, 18, 0, 0)
                self.add_calendar(home_team, away_team, game_date, 2, season_id)

    def create_generic_preseason(self, total_teams: list, start_date: str, end_date: str, season_id: int):
        random.shuffle(total_teams)
        num_days_diff, start_date_dated, end_date_dated = Utilities.diff_dates_in_days(start_date, end_date)
        num_games = int(num_days_diff / 4)
        days_for_game = int(num_days_diff / num_games)
        i = 0
        while i < num_games:
            teams_1 = total_teams[0: int((len(total_teams) / 2))]
            teams_2 = total_teams[int(len(total_teams) / 2):]
            for j in range(1, len(teams_1) + 1):
                self.generic_preseason_assign(start_date_dated, days_for_game, teams_1, teams_2, season_id, j)
            start_date_dated = start_date_dated + datetime.timedelta(days=days_for_game)
            i += 1

    def generic_season_assign(self, start_date: str, end_date: str, home_team_id: int, away_team_id: int,
                              season_id: int, season_info: Season):
        num_days_diff, start_date_dated, end_date_dated = Utilities.diff_dates_in_days(start_date, end_date)
        stadium_id = self.stadiums_info[home_team_id]
        assigned = False
        while not assigned:
            selected_date = start_date_dated + datetime.timedelta(days=random.randint(0, num_days_diff - 1))
            if not self.is_any_game_in_stadium(stadium_id, selected_date) and self.is_allowed_by_dates(home_team_id,
                                                                                                       away_team_id,
                                                                                                       selected_date,
                                                                                                       season_info):
                game_date = datetime.datetime(selected_date.year, selected_date.month, selected_date.day, 18, 0, 0)
                self.add_calendar(home_team_id, away_team_id, game_date, 3, season_id)
                assigned = True

    def create_generic_season(self, start_date: str, end_date: str, season_id: int, league_id: int, season_info: Season):
        for team_id in self.games[league_id]:
            opponents_list = self.games[league_id][team_id]
            random.shuffle(opponents_list)
            for opponent_id in opponents_list:
                self.generic_season_assign(start_date, end_date, team_id, opponent_id, season_id, season_info)

    def assign_season_generic_games(self, league_id: int, season_info: Season):
        if league_id in self.games and league_id in self.season_info:
            # Season Games
            self.fill_dates(season_info.season_start_date_id, season_info.season_end_date_id)
            self.create_generic_season(season_info.season_start_date_id, season_info.season_end_date_id,
                                       season_info.season_id, league_id, season_info)

    def assign_preseason_generic_games(self, league_id: int, season_info: Season):
        if league_id in self.games and league_id in self.season_info:
            # Preseason Games
            self.fill_dates(season_info.preseason_start_date_id, season_info.preseason_end_date_id)
            total_teams = list(self.games[league_id].keys())
            self.create_generic_preseason(total_teams, season_info.start_date_preseason,
                                          season_info.end_date_preseason, season_info.season_id)
