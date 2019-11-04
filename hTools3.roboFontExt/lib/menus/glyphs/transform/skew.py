# menuTitle : skew

from importlib import reload
import hTools3.dialogs.glyphs.skew
reload(hTools3.dialogs.glyphs.skew)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.glyphs.skew import SkewGlyphsDialog

OpenWindow(SkewGlyphsDialog)
