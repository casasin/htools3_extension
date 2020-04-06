# menuTitle : build glyphs

from importlib import reload
import hTools3.dialogs.batch.build
reload(hTools3.dialogs.batch.build)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.batch.build import BatchBuildGlyphsDialog

OpenWindow(BatchBuildGlyphsDialog)
