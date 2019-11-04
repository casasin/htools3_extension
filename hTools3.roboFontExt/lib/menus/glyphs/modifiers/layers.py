# menuTitle : layers

from importlib import reload
import hTools3.dialogs.glyphs.modifiersLayers
reload(hTools3.dialogs.glyphs.modifiersLayers)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.glyphs.modifiersLayers import SelectLayersDialog

OpenWindow(SelectLayersDialog)
