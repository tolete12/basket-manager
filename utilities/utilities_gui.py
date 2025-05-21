import configparser


from gui.my_combobox import MyCombobox
from utilities import Utilities
from variables import paths
from variables.constants import LEFT_ARROW, RIGHT_ARROW
from variables.paths import iconsPicsDir



class UtilitiesGui:

    

    @staticmethod
    def get_screen_size():
        width = 1280
        height = 720
        if Utilities.file_exists(paths.configFile):
            config = configparser.ConfigParser()
            config.read(paths.configFile)
            width = config['General']['WIDTH'] if int(config['General']['WIDTH']) >= 1280 else 1280
            height = config['General']['HEIGHT'] if int(config['General']['HEIGHT']) >= 720 else 720
        return int(width), int(height)

    