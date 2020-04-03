# menuTitle : condense

from importlib import reload
import hTools3.dialogs.glyphs.interpolationCondense
reload(hTools3.dialogs.glyphs.interpolationCondense)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.glyphs.interpolationCondense import CondenseGlyphsDialog

OpenWindow(CondenseGlyphsDialog)
