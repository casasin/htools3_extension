# menuTitle : rename

from importlib import reload
import hTools3.dialogs.glyphs.namesChange
reload(hTools3.dialogs.glyphs.namesChange)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.glyphs.namesChange import ChangeGlyphNamesDialog

OpenWindow(ChangeGlyphNamesDialog)
