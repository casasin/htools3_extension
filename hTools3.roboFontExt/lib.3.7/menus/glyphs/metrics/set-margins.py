# menuTitle : set margins

from importlib import reload
import hTools3.dialogs.glyphs.marginsSet
reload(hTools3.dialogs.glyphs.marginsSet)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.glyphs.marginsSet import SetMarginsDialog

OpenWindow(SetMarginsDialog)
