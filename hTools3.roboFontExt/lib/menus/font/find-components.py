# menuTitle : find components

from importlib import reload
import hTools3.dialogs.font.componentsFind
reload(hTools3.dialogs.font.componentsFind)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.font.componentsFind import FindGlyphComponentsDialog

OpenWindow(FindGlyphComponentsDialog)
