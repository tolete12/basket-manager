import os

from kivy.lang.builder import Builder
from kivymd.uix.screen import MDScreen

from utilities import Utilities


class LoadGame(MDScreen):
    cur_path = os.getcwd()
    separator = Utilities().get_separator()
    Builder.load_file(f"{cur_path}{separator}kv{separator}load_game.kv")
