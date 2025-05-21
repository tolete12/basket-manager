import os

from kivy.lang.builder import Builder
from kivymd.uix.screen import MDScreen

from utilities import Utilities


class MainMenu(MDScreen):
    cur_path = os.getcwd()
    separator = Utilities().get_separator()
    Builder.load_file(f"{cur_path}{separator}kv{separator}main_menu.kv")

    def load_new_career(self, screen_manager: str, *args):
        if args[0].last_touch.button == 'left':
            self.manager.current = screen_manager
