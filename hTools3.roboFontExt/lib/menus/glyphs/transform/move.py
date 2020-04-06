# menuTitle : move

from importlib import reload
import hTools3.dialogs.glyphs.move
reload(hTools3.dialogs.glyphs.move)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.glyphs.move import MoveGlyphsDialog

OpenWindow(MoveGlyphsDialog)
