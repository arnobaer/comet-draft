import os

VERSION = "1.0.0"

PACKAGE_DIR = os.path.dirname(__file__)

CONFIG_DIR = os.path.join(PACKAGE_DIR, "config")
SETUPS_DIR = os.path.join(CONFIG_DIR, "setups")
PLUGINS_DIR = os.path.join(PACKAGE_DIR, "plugins")

CONTENTS_URL = "https://example.com/"

__version__ = VERSION
