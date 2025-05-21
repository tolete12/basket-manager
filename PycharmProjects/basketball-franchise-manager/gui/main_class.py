from db.sql_lite_handler import SQLiteHandler
from db.sql_lite_helper import SQLLiteHelper
from utilities import Utilities
from utilities.utilities_gui import UtilitiesGui


class MainClass:
    option = 0
    db_obj = None
    sql_helper = None

    def __init__(self):
        self.utilities = Utilities(self.db_obj)
        self.get_language()
        self.size_x, self.size_y = UtilitiesGui.get_screen_size()

    def connect_db(self, db: str, override: bool, save_game: bool):
        self.db_obj = SQLiteHandler(db, override=override, save_game=save_game)
        self.sql_helper = SQLLiteHelper(self.db_obj)

    def close_db(self):
        self.db_obj.close_connection()

    def get_language(self):
        self.option = self.utilities.get_config_language()
