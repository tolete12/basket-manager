import os
import sys


sep = '\\' if sys.platform in ['win32', 'cygwin'] else '/'

fileDir = os.path.dirname(os.path.abspath(__file__))

parentDir = os.path.dirname(fileDir)

savegamesDir = parentDir + sep + "savegames"

ctlDir = parentDir + sep + "db" + sep + "ctl"

defaultrecordsDir = parentDir + sep + "db" + sep + "defaultrecords"

resourcesDir = parentDir + sep + "resources"

playersPicsDir = resourcesDir + sep + "pics" + sep + "players"

teamsPicsDir = resourcesDir + sep + "pics" + sep + "teams"

backgroundsPicsDir = resourcesDir + sep + "backgrounds"

iconsPicsDir = resourcesDir + sep + "icons"

configFile = parentDir + sep + "config.ini"
