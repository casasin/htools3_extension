# menuTitle : rotate

from importlib import reload
import hTools3.dialogs.glyphs.rotate
reload(hTools3.dialogs.glyphs.rotate)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.glyphs.rotate import RotateGlyphsDialog

OpenWindow(RotateGlyphsDialog)
