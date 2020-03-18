# menuTitle : copy margins

from importlib import reload
import hTools3.dialogs.glyphs.marginsCopy
reload(hTools3.dialogs.glyphs.marginsCopy)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.glyphs.marginsCopy import CopyMarginsDialog

OpenWindow(CopyMarginsDialog)
