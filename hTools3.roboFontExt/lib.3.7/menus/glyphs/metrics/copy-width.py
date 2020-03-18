# menuTitle : copy width

from importlib import reload
import hTools3.dialogs.glyphs.widthCopy
reload(hTools3.dialogs.glyphs.widthCopy)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.glyphs.widthCopy import CopyWidthDialog

OpenWindow(CopyWidthDialog)
