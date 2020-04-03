# menuTitle : lock widths

from importlib import reload
import hTools3.dialogs.glyphs.layersLock
reload(hTools3.dialogs.glyphs.layersLock)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.glyphs.layersLock import LockLayerWidthsDialog

OpenWindow(LockLayerWidthsDialog)
