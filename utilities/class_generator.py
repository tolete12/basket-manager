import kivy
import os
from kivy.app import App
from utilities import Utilities
from variables.paths import parentDir
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

kivy.require('1.9.0')


class ClassGenerator:
    @staticmethod
    def generate_class_from_kv(screen_manager: ScreenManager, full_file_path: str, class_name: str):
        Builder.load_file(full_file_path)
        f = open(full_file_path, "r")
        line = f.readline()
        tag = line[1:len(line) - 3]
        dynamic_class = type(tag, (Screen,), {})
        obj = dynamic_class(name=class_name)
        screen_manager.add_widget(obj)
        return screen_manager


# Create the App class
class ScreenApp(App):
    def build(self):
        # Get the current working directory
        separator = ('\\' if Utilities.is_windows_os() else '/')
        kv_dir = parentDir + separator + 'kv'
        # The ScreenManager controls moving between screens
        screen_manager = ScreenManager()
        file_list = [f.lower() for f in os.listdir(kv_dir)]  # Convert to lower case
        file_list.sort(reverse=False)
        for file in file_list:
            if file.endswith(".kv"):
                full_file_path = kv_dir + separator + file
                class_name = file.split('.')[0]
                screen_manager = ClassGenerator.generate_class_from_kv(screen_manager, full_file_path, class_name)

        return screen_manager


if __name__ == "__main__":
    # run the app
    sample_app = ScreenApp()
    sample_app.run()
