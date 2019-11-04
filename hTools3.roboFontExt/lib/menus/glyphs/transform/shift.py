# menuTitle : shift points

from importlib import reload
import hTools3.dialogs.glyphs.shiftPoints
reload(hTools3.dialogs.glyphs.shiftPoints)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.glyphs.shiftPoints import ShiftPointsDialog

OpenWindow(ShiftPointsDialog)
