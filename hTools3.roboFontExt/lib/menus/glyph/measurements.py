# menuTitle : measurements

from importlib import reload
import hTools3.dialogs.glyph.measureHandles
reload(hTools3.dialogs.glyph.measureHandles)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.glyph.measureHandles import MeasureHandlesTool

OpenWindow(MeasureHandlesTool)
