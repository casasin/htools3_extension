# menuTitle : print

from importlib import reload
import hTools3.dialogs.glyphs.namesPrint
reload(hTools3.dialogs.glyphs.namesPrint)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.glyphs.namesPrint import PrintGlyphNamesDialog

OpenWindow(PrintGlyphNamesDialog)
