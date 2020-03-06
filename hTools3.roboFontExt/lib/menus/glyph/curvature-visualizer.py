# menuTitle : visualize curvature

from importlib import reload
import hTools3.dialogs.glyph.curvatureVisualizer
reload(hTools3.dialogs.glyph.curvatureVisualizer)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.glyph.curvatureVisualizer import CurvatureVisualizerDialog

OpenWindow(CurvatureVisualizerDialog)
