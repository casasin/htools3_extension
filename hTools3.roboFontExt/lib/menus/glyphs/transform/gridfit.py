# menuTitle : gridfit

from importlib import reload
import hTools3.dialogs.glyphs.gridfit
reload(hTools3.dialogs.glyphs.gridfit)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.glyphs.gridfit import RoundToGridDialog

OpenWindow(RoundToGridDialog)
