from sqlite3 import Row


class Calendar:

    def __init__(self):
        self.calendar_id = 0
        self.team_id_1 = 0
        self.team_id_2 = 0
        self.stadium_id = 0
        self.score_away = 0
        self.score_home = 0
        self.date_id = 0
        self.game_time = ''
        self.temperature = 0
        self.weather_id = 0
        self.game_type_id = 0
        self.season_id = 0

    def fill_from_db(self, row: Row):
        for attribute in row.keys():
            setattr(self, attribute, row[attribute])
        # self.calendar_id = row['IDCALENDARIOS']
        # self.team_id_1 = row['IDEQUIPO1']
        # self.team_id_2 = row['IDEQUIPO2']
        # self.stadium_id = row['IDESTADIOS']
        # self.score_away = row['MARCADOR1']
        # self.score_home = row['MARCADOR2']
        # self.date_id = row['FECHA']
        # self.temperature = row['TEMPERATURA']
        # self.weather_id = row['IDCLIMAS']
        # self.game_type_id = row['IDTIPOSPARTIDOS']
        # self.season_id = row['IDTEMPORADAS']

    def fill_single_calendar(self, calendar_dict: dict):
        for key, value in calendar_dict.items():
            setattr(self, key, value)
        # self.calendar_id = calendar_dict['IDCALENDARIOS']
        # self.team_id_1 = calendar_dict['IDEQUIPO1']
        # self.team_id_2 = calendar_dict['IDEQUIPO2']
        # self.stadium_id = calendar_dict['IDESTADIOS']
        # self.score_away = calendar_dict['MARCADOR1']
        # self.score_home = calendar_dict['MARCADOR2']
        # self.date_id = calendar_dict['FECHA']
        # self.temperature = calendar_dict['TEMPERATURA']
        # self.weather_id = calendar_dict['IDCLIMAS']
        # self.game_type_id = calendar_dict['IDTIPOSPARTIDOS']
        # self.season_id = calendar_dict['IDTEMPORADAS']

