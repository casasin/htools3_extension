# menuTitle : import

from importlib import reload
import hTools3.dialogs.glyphs.layersImport
reload(hTools3.dialogs.glyphs.layersImport)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.glyphs.layersImport import ImportGlyphsIntoLayerDialog

OpenWindow(ImportGlyphsIntoLayerDialog)
