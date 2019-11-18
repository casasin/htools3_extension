# menuTitle : preferences

from importlib import reload
import hTools3.dialogs.preferences
reload(hTools3.dialogs.preferences)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.preferences import PreferencesDialog

OpenWindow(PreferencesDialog)
