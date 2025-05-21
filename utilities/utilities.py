import locale
import os
import configparser
import datetime
import sys
from datetime import date
import statsapi
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.spinner import Spinner
from kivymd.app import MDApp

from db.sql_lite_handler import SQLiteHandler
from db.sql_lite_helper import SQLLiteHelper
from variables import paths
from variables.constants import INI_DB


class ImageButton(ButtonBehavior, Image):
    pass


class Utilities:
    db_obj = None

    def __init__(self, db_obj=None):
        self.db_obj = db_obj

    def get_image_button(self):
        return ImageButton()

    @staticmethod
    def get_common_vars():
        app = MDApp.get_running_app()
        return {'translations': app.translations,
                'language_id': app.language_id,
                'sql_helper': app.sql_helper,
                'db_obj': app.db_obj,
                'my_popup': app.my_popup,
                'utilities': app.utilities
                }

    def get_separator(self):
        return '\\' if self.is_windows_os() else '/'

    def get_columns_from_ctl(self, table: str):
        sep = self.get_separator()
        file_path = paths.parentDir + sep + "db" + sep + "ctl" + sep + table
        print(file_path)
        file1 = open(file_path, 'r')
        lines = file1.readlines()
        columns = []
        for line in lines:
            line_split = line.split('"')
            print(line_split)
            if len(line_split) > 1:
                if not line_split[1] == table.upper() and not line_split[1]==table:
                    columns.append(line_split[1])
        return columns
    
    @staticmethod
    def create_football_matrix(attributes: list):
        positions = [
            'QB', 'FB', 'RB', 'TE', 'LT', 'LG', 'C', 'RG', 'RT', 'SE', 'FL', 'SL',
            'DE', 'DT', 'NT', 'MLB', 'ILB', 'OLB', 'SLB', 'WLB', 'CB', 'SS', 'FS',
            'K', 'P', 'LS'
        ]

        dict_matrix = {pos: {attr: {i: {'prob'} for i in range(1, 21)} for attr in attributes} for pos in positions}

        print(dict_matrix)

        return dict_matrix

        

    @staticmethod
    def set_dict_values_zero(column_list: list):
        dict_to_zero = {}
        for column in column_list:
            dict_to_zero[column] = 0
        return dict_to_zero

    @staticmethod
    def get_ctl_data(ctl_dir, filename):
        with open(ctl_dir + '/' + filename, 'r') as myFile:
            if os.path.getsize(ctl_dir + '/' + filename) > 0:
                return myFile.read()

    def get_mlb_schedule(self, year: int):
        sql_helper = SQLLiteHelper(self.db_obj)
        # print(statsapi.meta('gameTypes'))
        start_date = Utilities.convert_text_to_date(f"{str(year)}-03-01")
        end_date = Utilities.convert_text_to_date(f"{str(year)}-10-10")
        games = {}
        while start_date <= end_date:
            print(f"Processing {self.convert_date_to_text(start_date)}")
            if start_date not in games:
                games[start_date] = []

            schedule = statsapi.schedule(Utilities.convert_date_to_text(start_date))
            for match in schedule:
                if match['game_type'] == 'R':
                    games = self._map_match(sql_helper, match, games, start_date)
            start_date = start_date + datetime.timedelta(days=1)

        return games

    @staticmethod
    def is_windows_os():
        if sys.platform in ['win32', 'cygwin']:
            return True
        return False

    @staticmethod
    def get_root_path():
        cur_path = os.path.dirname(os.path.abspath(__file__))
        return cur_path.split("american-sports-manager")[0] + "american-sports-manager"

    def write_mlb_schedule_to_file(self, games: dict, year: int):
        root_path = self.get_root_path()
        file_path = f"{root_path}\db\mlb_schedule\mlb_{year}" if self.is_windows_os() else f"{root_path}/db/mlb_schedule/mlb_{year}"
        with open(file_path, 'w') as f:
            for date, game_list in games.items():
                for game in game_list:
                    f.write(f"{self.convert_date_to_text(date)}|{str(game[0])}|{str(game[1])}|{str(game[2])}")
                    f.write('\n')

    def _map_match(self, sql_helper, match, games, start_date):
        away_team_id = sql_helper.get_team_id_by_name(self._remap_old_team_names(match['away_name']))
        home_team_id = sql_helper.get_team_id_by_name(self._remap_old_team_names(match['home_name']))

        games[start_date].append((match['game_datetime'], away_team_id, home_team_id))
        return games

    @staticmethod
    def _remap_old_team_names(team_name: str):
        if team_name == 'Cleveland Indians':
            return 'Cleveland Guardians'
        if team_name == 'Florida Marlins':
            return 'Miami Marlins'
        return team_name

    @staticmethod
    def is_spanish():
        language = locale.getdefaultlocale()
        spanish = ['ES_AR', 'ES_CL', 'ES_CO', 'ES_MX', 'ES_PE', 'ES_PR', 'ES_ES', 'ES_VE']

        if language[0].upper() in spanish:
            return True
        else:
            return False

    @staticmethod
    def convert_text_to_date(date: str, format: str = "%Y-%m-%d"):
        return datetime.datetime.strptime(date, format).date()

    @staticmethod
    def convert_date_to_text(date: date, format: str = "%Y-%m-%d"):
        return date.strftime(format)

    @staticmethod
    def convert_datetime_to_text(date: date, format: str = "%Y-%m-%d %H:%M:%S"):
        return date.strftime(format)

    @staticmethod
    def diff_dates_in_days(start_date: str, end_date: str):
        start_date_dated = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_dated = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        time_between_dates = end_date_dated - start_date_dated
        days_between_dates = time_between_dates.days
        return days_between_dates, start_date_dated, end_date_dated

    def get_config_language(self):
        option = 2
        if self.file_exists(paths.configFile):
            config = configparser.ConfigParser()
            config.read(paths.configFile)
            option = config['General']['LANGUAGE']

        return int(option)

    def set_default_config(self):
        if not self.file_exists(paths.configFile):
            frame = Tk()
            screen_width = frame.winfo_screenwidth()
            if screen_width < 1280:
                screen_width = 1280
            screen_height = frame.winfo_screenheight()
            if screen_height < 720:
                screen_height = 720
            frame.destroy()

            f = open(paths.configFile, "w+")
            f.write("[General]\n")
            if self.is_spanish():
                f.write("LANGUAGE=1\n")
            else:
                f.write("LANGUAGE=2\n")
            f.write("WIDTH=" + str(screen_width) + "\n")
            f.write("HEIGHT=" + str(screen_height) + "\n")
            f.close()

    @staticmethod
    def get_translation(translations, translation_id, language_id):
        return translations[language_id][translation_id]

    @staticmethod
    def get_translation_id_from_text(translations, text, language_id):
        for key, value in translations[language_id].items():
            if value == text:
                return key

    def change_config_value(self, section, value=0):
        search = section + '='
        line_number = 0
        if self.file_exists(paths.configFile):
            with open(paths.configFile, 'r') as myFile:
                data = myFile.readlines()
                for num, line in enumerate(myFile, 1):
                    if search in line:
                        line_number = num

            data[line_number] = section + '=' + str(value)

            with open(paths.configFile, 'w') as file:
                file.writelines(data)

    def create_dropdown(self, items: list, pos_hint, size_hint, text):
        spinner = Spinner(
            values=items,
            size_hint=size_hint,
            pos_hint=pos_hint
        )

        return spinner

    @staticmethod
    def file_exists(file):
        if os.path.isfile(file):
            return True
        else:
            return False

    @staticmethod
    def list_files(directory, extension):
        file_list = [f for f in os.listdir(directory) if f.endswith('.' + extension)]
        file_list.sort()
        return file_list

    @staticmethod
    def say_hello():
        messagebox.showinfo("Say Hello", "Hello World")

    @staticmethod
    def test_record(option):
        db_obj = SQLiteHandler(INI_DB, override=False, save_game=False)
        sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='TRANSLATIONS';"
        rows = db_obj.read_records(sql)[0]

        if rows:
            sql = "SELECT text, translation_id FROM TRANSLATIONS WHERE translation_id = 1 AND language_id = " + str(
                option)
            print(sql)
            rows = db_obj.read_records(sql)[0]
            for row in rows:
                print(row[0])
                print(row['translation_id'])
                break
            override = False
        else:
            override = True
        return rows, override


    @staticmethod
    def get_pixels_from_lines(value):
        return int(value * 7.937)

    @staticmethod
    def get_lines_from_pixels(value):
        return int(value * 0.12599)

    @staticmethod
    def get_default_queries():
        queries_list = list()
        for filename in os.listdir(paths.defaultrecordsDir):
            with open(paths.defaultrecordsDir + '/' + filename, 'r') as myFile:
                if os.path.getsize(paths.defaultrecordsDir + '/' + filename) > 0:
                    for line in myFile:
                        queries_list.append(line)
        return queries_list

    @staticmethod
    def get_logos_per_row(size_x: int, team_logo_size_x: int):
        logos_per_row = int(size_x / team_logo_size_x)
        return logos_per_row - 1 if (logos_per_row * team_logo_size_x) + (logos_per_row * 20) else 0

    @staticmethod
    def get_initial_x_pos(logos_per_row: int, cur_row: int, len_rows: int, size_x: int, team_logo_size_x: int):
        initial_x_pos = 0
        if logos_per_row * (cur_row + 2) > len_rows:
            initial_x_pos = int((size_x - (team_logo_size_x * (len_rows - (cur_row * logos_per_row))) - (
                    20 * (len_rows - 1 - (cur_row * logos_per_row)))) / 2)
        if len_rows >= (cur_row + 1) * logos_per_row:
            initial_x_pos = int(
                (size_x - (team_logo_size_x * logos_per_row) - (20 * (logos_per_row - 1))) / 2)
        return initial_x_pos

    @staticmethod
    def get_screen_size():
        # if platform.lower() in ['android', 'macosx']:
        width = 1280
        height = 720
        if Utilities.file_exists(paths.configFile):
            config = configparser.ConfigParser()
            config.read(paths.configFile)
            width = config['General']['WIDTH'] if int(config['General']['WIDTH']) >= 1280 else 1280
            height = config['General']['HEIGHT'] if int(config['General']['HEIGHT']) >= 720 else 720
        return int(width), int(height)

    @staticmethod
    def get_screen_window_size():
        """Get the screen size in a cross-platform way."""
        try:
            # Try using ImageGrab first (works on Windows and macOS)
            import PIL.ImageGrab
            return PIL.ImageGrab.grab().size
        except (ImportError, OSError):
            # Fall back to screeninfo for Linux
            from screeninfo import get_monitors
            monitor = get_monitors()[0]  # Primary monitor
            return (monitor.width, monitor.height)

    @staticmethod
    def position_center_window(width_window, height_window):
        screen_width, screen_height = Utilities.get_screen_window_size()
        return (int(screen_width) - int(width_window)) / 2, (int(screen_height) - int(height_window)) / 2,


if __name__ == '__main__':
    columns = Utilities().get_columns_from_ctl("players")
    attributes = Utilities.create_football_matrix(columns)
    print(attributes)
