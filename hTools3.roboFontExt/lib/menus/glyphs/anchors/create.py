# menuTitle : create anchors

from importlib import reload
import hTools3.dialogs.glyphs.anchorsCreate
reload(hTools3.dialogs.glyphs.anchorsCreate)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.glyphs.anchorsCreate import CreateAnchorsDialog

OpenWindow(CreateAnchorsDialog)
