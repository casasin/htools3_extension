# menuTitle : interpolate

from importlib import reload
import hTools3.dialogs.glyphs.interpolationMasters
reload(hTools3.dialogs.glyphs.interpolationMasters)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.glyphs.interpolationMasters import InterpolateGlyphsDialog

OpenWindow(InterpolateGlyphsDialog)
