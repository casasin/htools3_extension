# menuTitle : actions

from importlib import reload
import hTools3.dialogs.glyphs.actions
reload(hTools3.dialogs.glyphs.actions)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.glyphs.actions import GlyphActionsDialog

OpenWindow(GlyphActionsDialog)