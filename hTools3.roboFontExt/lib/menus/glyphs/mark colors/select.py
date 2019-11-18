# menuTitle : mark & select

from importlib import reload
import hTools3.dialogs.glyphs.markSelect
reload(hTools3.dialogs.glyphs.markSelect)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.glyphs.markSelect import MarkGlyphsDialog

OpenWindow(MarkGlyphsDialog)
