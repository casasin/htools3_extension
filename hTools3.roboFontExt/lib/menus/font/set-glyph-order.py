# menuTitle: set glyph order

from importlib import reload
import hTools3.dialogs.font.setGlyphOrder 
reload(hTools3.dialogs.font.setGlyphOrder)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.font.setGlyphOrder import SetGlyphOrderDialog

OpenWindow(SetGlyphOrderDialog)

