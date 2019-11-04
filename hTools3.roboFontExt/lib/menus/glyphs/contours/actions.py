from importlib import reload
import hTools3.dialogs.glyphs.actions
reload(hTools3.dialogs.glyphs.actions)

from hTools3.dialogs.glyphs.actions import GlyphActionsDialog
from mojo.roboFont import OpenWindow

OpenWindow(GlyphActionsDialog)