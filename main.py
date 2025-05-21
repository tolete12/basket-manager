# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.


import datetime

from kivy.clock import Clock
from kivy.properties import DictProperty
from kivy.uix.screenmanager import ScreenManager, FadeTransition, NoTransition

from db.createrecords.calendars.create_nba_calendar import CreateNBACalendar
import gui.main_class as main_class
from db.initial_database_handler import InitialDatabaseHandler
from kv.splash_screen import SplashScreen
from variables.constants import GAME_NAME, INI_DB
from kivy.config import Config
from utilities import Utilities
from utilities.kv_utilities import MyPopUp

width = 1440
height = 800
pos_x, pos_y = Utilities().position_center_window(width, height)
Config.set('graphics', 'resizable', True)
Config.set('input', 'mouse', 'mouse,disable_multitouch')
from kivy.core.window import Window
from kivymd.app import MDApp

Window.size = (int(width), int(height))

class Manager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MainApp(MDApp, main_class.MainClass):
    screen_manager = Manager(transition=FadeTransition(duration=0.25))
    translations = DictProperty()
    language_id = Utilities().get_config_language()
    my_popup = MyPopUp(translations, language_id)
    main_class.MainClass().__init__()

    def redefine_db_object(self, override, save_game):
        super().connect_db(INI_DB, override, save_game)

    def update_translations_obj(self):
        self.translations = self.sql_helper.get_all_translations()

    def update_popup_obj(self):
        self.my_popup = MyPopUp(self.translations, self.language_id)

    def update_objects(self):
        self.update_translations_obj()
        self.update_popup_obj()

    def start_init_actions(self):
        rows, override = Utilities.test_record(1)
        override = True

        save_game = False
        super().connect_db(INI_DB, override, save_game)

        initial_db_handler = InitialDatabaseHandler(self.db_obj, self.utilities, self.sql_helper)
        self.utilities.set_default_config()
        if override:
            initial_db_handler.create_tables()
            initial_db_handler.insert_default_records(1900, datetime.date.today().year + 1)
            self.create_records()

    def create_records(self):
        season_info = self.sql_helper.get_latest_seasons_info()[1]
        calendar = CreateNBACalendar(self.sql_helper, self.sql_helper.get_stadium_per_team(), self.translations)
        calendar.create_nba_calendar()
        calendar.assign_season_generic_games(1, season_info)
        print("calendar ok")
        
        

    @staticmethod
    def window_size():
        Window.size_hint_y = None
        Window.top = 0
        Window.left = pos_x

    def build(self):
        # Set App Title
        self.title = GAME_NAME
        # Set App Theme
        # self.theme_cls.primary_palette = 'Gray'
        # self.theme_cls.theme_style = 'Dark'

        self.screen_manager = Manager(transition=NoTransition(duration=0.25))
        self.screen_manager.add_widget(SplashScreen())
        self.window_size()
        self.start_init_actions()

        self.load_widgets()

        print("ok")
        # Return screen manager
        return self.screen_manager

    def load_widgets(self):
        import glob
        import importlib
        import os

        current_dir = os.path.join(os.path.dirname(os.path.abspath(__file__))) + Utilities().get_separator() + "kv"
        current_module_name = os.path.splitext(os.path.basename(current_dir + Utilities().get_separator() + "kv"))[0]
        for file in glob.glob(current_dir + "/*.py"):
            name = os.path.splitext(os.path.basename(file))[0]

            # Ignore __ files
            if name.startswith("__") or name == 'splash_screen':
                continue
            module = importlib.import_module("." + name, package=current_module_name)

            for key, value in module.__dict__.items():
                if str(value).startswith("<class 'kv"):
                    module = importlib.import_module("kv." + name)
                    my_class = getattr(module, key)
                    my_instance = my_class()
                    self.screen_manager.add_widget(my_instance)

    def on_start(self):
        # Delay time for splash screen before transitioning to main screen
        super().on_start()
        Clock.schedule_once(self.change_screen, 6)  # Delay for 10 seconds

    def change_screen(self, dt):
        self.screen_manager.current = "MainMenu"


if __name__ == '__main__':
    MainApp().run()
