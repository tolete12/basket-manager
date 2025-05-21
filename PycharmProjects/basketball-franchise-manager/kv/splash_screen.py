import os

from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from utilities import Utilities


class SplashScreen(MDScreen):
    cur_path = os.getcwd()
    separator = Utilities().get_separator()
    Builder.load_file(f"{cur_path}{separator}kv{separator}splash_screen.kv")
