# menuTitle : scale

from importlib import reload
import hTools3.dialogs.glyphs.scale
reload(hTools3.dialogs.glyphs.scale)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.glyphs.scale import ScaleGlyphsDialog

OpenWindow(ScaleGlyphsDialog)
