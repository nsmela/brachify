# ref: 

from pathlib import Path 

APP_NAME = "brachify"
VERSION_MAJOR = "0"
VERION_MINOR = "3"
APP_VERSION = "alpha"

# Application Paths
DIR_PATH = Path(__file__).parent  # src folder location

HOME_PATH = Path.home()
USER_PATH = HOME_PATH.joinpath(APP_NAME)
RESOURCES_PATH = DIR_PATH.joinpath("resources")

