# menuTitle : set style data

from importlib import reload
import hTools3.dialogs.batch.setStyleData
reload(hTools3.dialogs.batch.setStyleData)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.batch.setStyleData import BatchSetStyleDataDialog

OpenWindow(BatchSetStyleDataDialog)
