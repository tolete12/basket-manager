from datetime import date
from db.sql_lite_handler import SQLiteHandler
from models.season import Season
from variables.constants import TEXTO, TRANSLATIONS_TABLE, TRANSLATION_ID, LANGUAGE_ID, VALUE, ID, ABBREV_ID
from variables.constants import INI_DB


class SQLLiteHelper:
    def __init__(self, db_obj: SQLiteHandler):
        self.db_obj = db_obj

    def insert_records_handler(self, table: str, list_values: list):
        sql = f"INSERT INTO {table} VALUES ("
        for _ in list_values:
            sql += "?,"
        size = len(sql)
        # Slice string to remove last 2 characters from string
        mod_sql = sql[:size - 1] + ");"
        self.db_obj.insert_records_with_cursor(mod_sql, list_values)

    @staticmethod
    def _add_dynamic_filters(filtered_fields: list, filtered_values: list, is_filter_str: list):
        sql_filter = " WHERE "
        for filter_index in range(len(filtered_fields)):
            filter_loop = f"{filtered_fields[filter_index]} = '{filtered_values[filter_index]}'" if \
                is_filter_str[filter_index] else f"{filtered_fields[filter_index]} = {filtered_values[filter_index]}"
            if filter_index > 0:
                filter_loop = " AND " + filter_loop
            sql_filter += filter_loop
        return sql_filter

    def update_specific_cell(self, table: str, fields: list, values: list, filtered_fields: list,
                             filtered_values: list, is_value_str: list, is_filter_str: list):
        if len(fields) == len(values):
            for index in range(len(fields)):
                sql_filter = ''
                if filtered_fields:
                    sql_filter = self._add_dynamic_filters(filtered_fields, filtered_values, is_filter_str)
                value = f"'{values[index]}'" if is_value_str[index] else values[index]
                sql = f"UPDATE {table} SET {fields[index]} = {value} {sql_filter}"
                self.db_obj.execute_query(sql)
            self.db_obj.commit_db()

    def get_all_names(self, country_id: int = 1):
        sql = f"SELECT name_id, name, odds FROM NAMES WHERE country_id = {country_id}"
        rows = self.db_obj.read_records(sql)
        name_dict = {}
        for row in rows[0]:
            name_dict[row['name_id'] + '-' + row['name']] = row['odds']
        return name_dict

    def get_all_surnames(self, country_id: int = 1):
        sql = f"SELECT surname_id, surname, odds FROM SURNAMES WHERE country_id = {country_id}"
        rows = self.db_obj.read_records(sql)
        surname_dict = {}
        for row in rows:
            surname_dict[row['surname_id'] + '-' + row['surname']] = row['odds']
        return surname_dict

    def get_all_translations(self):
        sql = "SELECT translation_id, language_id, text FROM TRANSLATIONS ORDER BY 2,1"
        rows, cursor = self.db_obj.read_records(sql)
        translations = {row['language_id']: {row_data['translation_id']: row_data['text'] for row_data in
                                             list(filter(lambda x: x['language_id'] == row['language_id'], rows))} for
                        row in rows}
        return translations

    def get_latest_season_id(self, league_id: int):
        sql = "SELECT MAX(season_id) AS max_season_id FROM SEASONS WHERE league_id = " + str(league_id)
        rows = self.db_obj.read_records(sql)
        return rows[0]['max_season_id']

    def get_max_calendar_id(self):
        sql = "SELECT MAX(season_id) AS max_season_id FROM SEASONS"
        rows = self.db_obj.read_records(sql)
        if rows[0][0]['max_season_id']:
            return rows[0][0]['max_season_id']
        return 0

    def get_max_id(self, field: str, table: str):
        sql = f"SELECT MAX({field}) AS MAX_ID FROM {table}"
        rows, _ = self.db_obj.read_records(sql)
        if rows[0]['MAX_ID']:
            return rows[0]['MAX_ID']
        return 0

    def get_team_id_by_name(self, name: str):
        sql = "SELECT team_id FROM teams WHERE name = '" + name + "'"
        rows = self.db_obj.read_records(sql)
        return rows[0]['team_id']

    def get_team_name_by_id(self, team_id: int):
        sql = "SELECT name FROM TEAMS WHERE team_id = " + str(team_id)
        rows = self.db_obj.read_records(sql)
        return rows[0][0]['name']

    def get_latest_seasons_info(self):
        sql = "SELECT * FROM SEASONS WHERE season_id IN (SELECT MAX(season_id) FROM SEASONS GROUP BY " \
              "league_id) "
        rows = self.db_obj.read_records(sql)
        season_info = {}
        for row in rows[0]:
            season_info[row['league_id']] = Season().load_from_db(row)
        return season_info
    
    def get_stadium_per_team(self):
        sql = "SELECT team_id, stadium_id FROM TEAMS"
        rows = self.db_obj.read_records(sql)
        stadiums_info = {}
        for row in rows[0]:
            stadiums_info[row['team_id']] = row['stadium_id']
        return stadiums_info

    def get_latest_standings(self, league_id: int, value: int, text_id: str):
        max_season_id = self.get_latest_season_id(league_id)

        sql = "SELECT * FROM STANDINGS WHERE "
        if text_id == "div":
            sql += "division_id = " + str(value)
        if text_id == "conf":
            sql += "conference_id = " + str(value)
        if text_id == "league":
            sql += "league_id = " + str(value)
        sql += " AND season_id = " + str(max_season_id)
        sql += " ORDER BY (wins-loses) DESC, wins DESC, winning_percentage DESC"

        rows = self.db_obj.read_records(sql)

        return rows

    def get_div_with_teams_hierarchy(self, league_id, hierarchy_id):
        sql = "SELECT " + hierarchy_id + " AS " + ID + ", TEAMS.team_id AS " + VALUE + \
              " FROM TEAMS INNER JOIN DIVISIONS ON TEAMS.division_id = DIVISIONS.division_id" \
              " INNER JOIN CONFERENCES ON CONFERENCES.conference_id = DIVISIONS.conference_id" \
              " INNER JOIN LEAGUES ON LEAGUES.league_id = CONFERENCES.league_id" \
              " WHERE LEAGUES.league_id = " + league_id
        rows = self.db_obj.read_records(sql)
        records = {}
        for row in rows[0]:
            if row[ID] in records.keys():
                records[row[ID]].append(row[VALUE])
            else:
                records[row[ID]] = [row[VALUE]]
        return records

    def get_teams_by_league(self, league_id: int):
        sql = "SELECT TEAMS.team_id AS team_id" \
              " FROM TEAMS INNER JOIN DIVISIONS ON TEAMS.division_id = DIVISIONS.division_id" \
              " INNER JOIN CONFERENCES ON CONFERENCES.conference_id = DIVISIONS.conference_id" \
              " INNER JOIN LEAGUES ON LEAGUES.league_id = CONFERENCES.league_id" \
              " WHERE LEAGUES.league_id = " + str(league_id)
        rows = self.db_obj.read_records(sql)
        return [row['league_id'] for row in rows]

    def get_date_id_from_date(self, selected_date: date):
        sql = f"SELECT date_id FROM DATES WHERE date = '{selected_date}'"
        rows = self.db_obj.read_records(sql)
        return rows[0][0]['date_id']

    def get_div_conf_with_teams_hierarchy(self, league_id, preseason=False):
        base_sql = "SELECT CONFERENCES.conference_id AS conference_id, DIVISIONS.division_id AS division_id, " \
                   " LEAGUES.league_id AS league_id, TEAMS.team_id " + \
                   " FROM TEAMS INNER JOIN DIVISIONS ON TEAMS.{} = DIVISIONS.division_id" \
                   " INNER JOIN CONFERENCES ON CONFERENCES.conference_id = DIVISIONS.conference_id" \
                   " INNER JOIN LEAGUES ON LEAGUES.league_id = CONFERENCES.league_id" \
                   " WHERE LEAGUES.league_id = " + league_id + " ORDER BY 1,2,3"
        if preseason:
            sql = base_sql.format("preseason_division_id")
        else:
            sql = base_sql.format("division_id")

        rows = self.db_obj.read_records(sql)
        conferences = list(set([row['conference_id'] for row in rows[0]]))
        records = {}
        dict_divisions = {}
        for conference_id in conferences:
            divisions = list(set(record['division_id']
                                 for record in list(filter(lambda x: x['conference_id'] == conference_id, rows[0]))))
            for division_id in divisions:
                teams = [record['team_id']
                         for record in list(filter(lambda x: x['division_id'] == division_id, rows[0]))]
                dict_divisions[division_id] = teams

            records[conference_id] = dict_divisions
            dict_divisions = {}
        return records

    def get_teams_by_conferences(self, league_id):
        sql = "SELECT CONFERENCES.conference_id AS " + ID + ", TEAMS.team_id AS " + VALUE + \
              " FROM TEAMS INNER JOIN DIVISIONS ON TEAMS.division_id = DIVISIONS.division_id" \
              " INNER JOIN CONFERENCES ON CONFERENCES.conference_id = DIVISIONS.conference_id" \
              " INNER JOIN LEAGUES ON LEAGUES.league_id = CONFERENCES.league_id" \
              " WHERE LEAGUES.league_id = " + league_id
        rows = self.db_obj.read_records(sql)
        records = {}
        for row in rows:
            if row[ID] in records.keys():
                records[row[ID]].append(row[VALUE])
            else:
                records[row[ID]] = [row[VALUE]]
        return records

    def get_single_field_translated(self, field_id: str, table: str, option: int, field_filtered: str = "",
                                    value_filtered: str = "", abbrev: bool = False) -> dict:

        sql = "SELECT " + field_id + " AS " + ID + ", " + TEXTO + " AS " + VALUE + \
              " FROM " + TRANSLATIONS_TABLE + \
              " AS TR INNER JOIN " + table + " AS A1 ON TR." + TRANSLATION_ID + " = " + "A1." + (
                  ABBREV_ID if abbrev else TRANSLATION_ID) + " WHERE TR.language_id = " + str(option)
        if field_filtered and value_filtered:
            sql += " AND A1." + field_filtered + " = " + \
                   (str(value_filtered) if isinstance(value_filtered, int) else '' + value_filtered + '')
        sql += " ORDER BY 2;"
        rows = self.db_obj.read_records(sql)
        return {row[VALUE]: row[ID] for row in rows}

    def get_id_and_field(self, field_id: str, field: str, table: str, field_filtered: str = "",
                         value_filtered: str = ""):
        sql = "SELECT " + field_id + ", " + field + " FROM " + table + " WHERE " + field_filtered + " = " + \
              (str(value_filtered) if isinstance(value_filtered, int) else '' + value_filtered + '') + " ORDER BY 2;"
        rows = self.db_obj.read_records(sql)
        return {row[field_id]: row[field] for row in rows}

    def get_league_id_by_abrev(self, value_filtered: str = ""):
        sql = "SELECT A2.league_id AS league_id FROM TRANSLATIONS A1 INNER JOIN LEAGUES A2 " \
              "ON A2.abbrev_id = A1.translation_id WHERE text = '" + value_filtered.replace("'", "''") + "'"
        rows = self.db_obj.read_records(sql)
        return rows[0][0]['league_id']

    def get_players_by_team_id(self, team_id):
        sql = "SELECT * FROM PLAYERS WHERE team_id = " + str(team_id)
        rows = self.db_obj.read_records(sql)
        return rows

    def get_sports_and_leagues(self, preseason: int = 0):
        query = "SELECT dep.sport_id AS sport_id, dep.translation_id, lig.league_id AS league_id, lig.abbrev_id, lig.popularity AS popularity " \
                "FROM SPORTS dep " \
                "INNER JOIN LEAGUES lig " \
                "ON dep.sport_id AND lig.sport_id " \
                "WHERE lig.preseason = " + str(preseason)
        cursor = self.db_obj.read_records(query)
        return cursor

    def get_sports_hierarchy(self):
        query = "SELECT dep.sport_id AS sport_id, dep.translation_id, " \
                "lig.league_id AS league_id, lig.abbrev_id as abbrev_id_leag, " \
                "conf.conference_id AS conference_id, conf.abbrev_id as abbrev_id_conf, " \
                "div.division_id AS division_id, div.abbrev_id as abbrev_id_div, " \
                "team.team_id," \
                "coun.country_id, coun.translation_id as country_trans_id " \
                "FROM DIVISIONS div " \
                "INNER JOIN CONFERENCES conf " \
                "ON conf.conference_id = div.conference_id " \
                "INNER JOIN LEAGUES lig " \
                "ON lig.league_id = conf.league_id " \
                "INNER JOIN SPORTS dep " \
                "ON dep.sport_id = lig.sport_id " \
                "INNER JOIN COUNTRIES coun " \
                "ON coun.country_id = lig.country_id " \
                "INNER JOIN TEAMS team " \
                "ON team.division_id = div.division_id " \
                "WHERE lig.preseason = 0"
        cursor = self.db_obj.read_records(query)
        return cursor

    def get_team_general_info(self):
        query = "SELECT dep.sport_id AS sport_id, lig.league_id AS league_id, " \
                "conf.conference_id AS conference_id, div.division_id AS division_id, " \
                "eqs.team_id AS team_id " \
                "FROM TEAMS eqs " \
                "INNER JOIN DIVISIONS div" \
                "ON div.division_id = eqs.division_id " \
                "INNER JOIN CONFERENCES conf" \
                "ON conf.conference_id = div.conference_id " \
                "INNER JOIN LEAGUES lig " \
                "ON lig.league_id = conf.league_id " \
                "INNER JOIN SPORTS dep " \
                "ON dep.sport_id = lig.sport_id"
        cursor = self.db_obj.read_records(query)
        return cursor

    def get_all(self, table):
        sql = f"SELECT * FROM {table};"
        rows = self.db_obj.read_records(sql)
        return rows
