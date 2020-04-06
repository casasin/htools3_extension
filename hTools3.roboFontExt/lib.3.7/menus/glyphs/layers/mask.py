# menuTitle : mask

from importlib import reload
import hTools3.dialogs.glyphs.layersMask
reload(hTools3.dialogs.glyphs.layersMask)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.glyphs.layersMask import MaskDialog

OpenWindow(MaskDialog)
