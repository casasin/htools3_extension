# menuTitle : find replace

from importlib import reload
import hTools3.dialogs.glyphs.namesFindReplace
reload(hTools3.dialogs.glyphs.namesFindReplace)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.glyphs.namesFindReplace import FindReplaceGlyphNamesDialog

OpenWindow(FindReplaceGlyphNamesDialog)
