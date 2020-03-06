# menuTitle : interpolation preview

from importlib import reload
import hTools3.dialogs.glyph.interpolationPreview
reload(hTools3.dialogs.glyph.interpolationPreview)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.glyph.interpolationPreview import InterpolationPreviewDialog

OpenWindow(InterpolationPreviewDialog)
