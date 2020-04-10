# menuTitle : clear data

from importlib import reload
import hTools3.dialogs.font.clearData
reload(hTools3.dialogs.font.clearData)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.font.clearData import ClearFontDataDialog

OpenWindow(ClearFontDataDialog)
