# menuTitle : set width

from importlib import reload
import hTools3.dialogs.glyphs.widthSet
reload(hTools3.dialogs.glyphs.widthSet)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.glyphs.widthSet import SetWidthDialog

OpenWindow(SetWidthDialog)
