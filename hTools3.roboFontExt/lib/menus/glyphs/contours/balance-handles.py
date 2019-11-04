# menuTitle : balance handles

from importlib import reload
import hTools3.dialogs.glyphs.balanceHandles
reload(hTools3.dialogs.glyphs.balanceHandles)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.glyphs.balanceHandles import BalanceHandlesDialog

OpenWindow(BalanceHandlesDialog)
