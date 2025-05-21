from sqlite3 import Row


class Season:
    season_id = 0
    name = ''
    league_id = 0
    start_date_preseason = ''
    end_date_preseason = ''
    start_date_season = ''
    end_date_season = ''
    start_date_playoffs = ''
    end_date_playoffs = ''
    draft_date_1 = ''
    draft_date_2 = ''
    draft_date_3 = ''
    start_date_whole_season = ''
    end_date_whole_season = ''
    draft_rounds = 0
    salary_cap = 0
    mid_level = 0
    biannual = 0
    num_weeks = 0
    min_bye_week = 0
    max_bye_week = 0
    all_star_start = ''
    all_star_end = ''

    def load_from_db(self, row: Row):
        for attribute in row.keys():
            setattr(self, attribute, row[attribute])
        # self.season_id = row['IDTEMPORADAS']
        # self.name = row['NOMBRE']
        # self.league_id = row['IDLIGAS']
        # self.start_date_preseason = row['FECHA_INICIO_PRESEASON']
        # self.end_date_preseason = row['FECHA_FIN_PRESEASON']
        # self.start_date_season = row['FECHA_INICIO_SEASON']
        # self.end_date_season = row['FECHA_FIN_SEASON']
        # self.start_date_playoffs = row['FECHA_INICIO_PLAYOFFS']
        # self.end_date_playoffs = row['FECHA_FIN_PLAYOFFS']
        # self.draft_date_1 = row['FECHA_DRAFT1']
        # self.draft_date_2 = row['FECHA_DRAFT2']
        # self.draft_date_3 = row['FECHA_DRAFT3']
        # self.start_date_whole_season = row['FECHA_INICIO_TEMPORADA']
        # self.end_date_whole_season = row['FECHA_FIN_TEMPORADA']
        # self.draft_rounds = row['NUM_RONDAS_DRAFT']
        # self.salary_cap = row['LIMITE_SALARIAL']
        # self.mid_level = row['MIDLEVEL']
        # self.biannual = row['BIANNUAL']
        # self.num_weeks = row['NUM_WEEKS']
        # self.min_bye_week = row['MIN_BYE_WEEK']
        # self.max_bye_week = row['MAX_BYE_WEEK']
        # self.all_star_start = row['ALL_STAR_START']
        # self.all_star_end = row['ALL_STAR_END']
        return self
