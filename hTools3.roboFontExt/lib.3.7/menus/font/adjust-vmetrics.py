# menuTitle : vertical metrics

from importlib import reload
import hTools3.dialogs.font.adjustVerticalMetrics
reload(hTools3.dialogs.font.adjustVerticalMetrics)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.font.adjustVerticalMetrics import AdjustVerticalMetricsDialog

OpenWindow(AdjustVerticalMetricsDialog)
