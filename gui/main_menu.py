import datetime

from kivy.lang import Builder
from kivy.properties import DictProperty, StringProperty
from kivy.uix.screenmanager import Screen

import gui.main_class as main_class
import gui.new_career as new_career
import gui.load_game as load_game
from db.initial_database_handler import InitialDatabaseHandler
from utilities import Utilities
from utilities.utilities_gui import UtilitiesGui
from variables.constants import BACKGROUND_SPORTS, BACKGROUND_PARQUE, INI_DB, GAME_NAME
from variables.paths import backgroundsPicsDir


class MainMenu(main_class.MainClass):
    root = None

    def __init__(self, override: bool = False, save_game: bool = False, first: bool = False):
        super().__init__()
        super().connect_db(INI_DB, override, save_game)
        self.override = override
        self.initial_db_handler = InitialDatabaseHandler(self.db_obj, self.utilities, self.sql_helper)
        if first:
            self.start_init_actions()
        self.translations = self.sql_helper.get_all_translations()
        self.language_id = Utilities().get_config_language()

    @staticmethod
    def hello():
        print("Hello algo")

    def start_init_actions(self):
        self.utilities.set_default_config()
        if self.override:
            self.initial_db_handler.create_tables()
            self.initial_db_handler.insert_default_records(1900, datetime.date.today().year)
            self.create_records()

    def create_records(self):
        pass
    #
    # def interface_main_menu(self):
    #     self.root, canvas = UtilitiesGui.set_center_window(self.size_x, self.size_y,
    #                                                        backgroundsPicsDir + BACKGROUND_PARQUE, GAME_NAME)
    #     my_font = font.Font(root=self.root, family="Helvetica", size=22, weight="bold")
    #
    #     pic_size_x = int(self.size_x / 1.3)
    #     pic_size_y = int(self.size_y / 1.3)
    #     img = UtilitiesGui.create_photo_image(backgroundsPicsDir + BACKGROUND_SPORTS, pic_size_x, pic_size_y)
    #     canvas.create_image(20, 20, anchor=NW, image=img)  # 20, 20 coordinates
    #
    #     but_pos_x = pic_size_x + (int(self.size_x - pic_size_x) / 8)
    #     UtilitiesGui.create_button(canvas, self.utilities.get_translation(self.translations, 22, self.option), my_font,
    #                                self.utilities.say_hello, {'bg': '#0AAE30', 'fg': 'white'},
    #                                {'pos_x': but_pos_x, 'pos_y': 20, 'height': 50})
    #     UtilitiesGui.create_button(canvas, self.utilities.get_translation(self.translations, 23, self.option), my_font,
    #                                self.utilities.say_hello, {'bg': '#A877BA', 'fg': 'white'},
    #                                {'pos_x': but_pos_x, 'pos_y': 100, 'height': 50})
    #     UtilitiesGui.create_button(canvas, self.utilities.get_translation(self.translations, 21, self.option), my_font,
    #                                self.go_to_new_career, {'bg': 'blue', 'fg': 'white'},
    #                                {'pos_x': but_pos_x, 'pos_y': 180, 'height': 50})
    #     UtilitiesGui.create_button(canvas, self.utilities.get_translation(self.translations, 20, self.option), my_font,
    #                                self.go_to_load_career, {'bg': 'blue', 'fg': 'white'},
    #                                {'pos_x': but_pos_x, 'pos_y': 260, 'height': 50})
    #     UtilitiesGui.create_button(canvas, self.utilities.get_translation(self.translations, 24, self.option), my_font,
    #                                self.utilities.say_hello, {'bg': '#A55200', 'fg': 'white'},
    #                                {'pos_x': but_pos_x, 'pos_y': 340, 'height': 50})
    #     UtilitiesGui.create_button(canvas, self.utilities.get_translation(self.translations, 25, self.option), my_font,
    #                                self.utilities.say_hello, {'bg': '#A55200', 'fg': 'white'},
    #                                {'pos_x': but_pos_x, 'pos_y': 420, 'height': 50})
    #
    #     UtilitiesGui.create_button(canvas, self.utilities.get_translation(self.translations, 154, self.option), my_font,
    #                                self.close_win, {'bg': 'red', 'fg': 'white'},
    #                                {'pos_x': but_pos_x, 'pos_y': 420, 'height': 50})
    #
    #     self.root.mainloop()

    def close_win(self):
        answer = askyesno(title=self.utilities.get_translation(self.translations, 155, self.option),
                          message=self.utilities.get_translation(self.translations, 156, self.option))
        if answer:
            self.root.destroy()

    def go_to_new_career(self):
        self.root.destroy()
        new_career.NewCareer(False, False, self.translations)

    def go_to_load_career(self):
        self.root.destroy()
        load_game.LoadGame(False, False, self.translations)


if __name__ == '__main__':
    start = MainMenu(override=True, save_game=False, first=True)
