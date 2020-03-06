# menuTitle : linked points

from importlib import reload
import hTools3.dialogs.glyph.linkPoints
reload(hTools3.dialogs.glyph.linkPoints)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.glyph.linkPoints import LinkPointsTool

OpenWindow(LinkPointsTool)
