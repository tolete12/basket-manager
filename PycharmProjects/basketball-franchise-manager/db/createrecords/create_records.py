import utilities


class CreateRecords:
    id_league = 0
    id_sport = 0
    db_obj = None
    cursor_teams = None
    utilities = None

    def __init__(self, db_obj, sports_and_leagues):
        self.db_obj = db_obj
        self.utilities = utilities.Utilities(self.db_obj)
        self.sports_and_leagues = sports_and_leagues

    def process_creation(self):
        for row in self.sports_and_leagues:
            self.get_teams(row)
            self.create_players(row)
        self.sports_and_leagues.close()

    def get_teams(self, row):
        self.cursor_teams = self.db_obj.get_team_general_info()

    def create_players(self, row):
        pass
