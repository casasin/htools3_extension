# menuTitle : build constructions

from importlib import reload
import hTools3.dialogs.glyphs.buildConstructions
reload(hTools3.dialogs.glyphs.buildConstructions)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.glyphs.buildConstructions import BuildConstructionDialog

OpenWindow(BuildConstructionDialog)
