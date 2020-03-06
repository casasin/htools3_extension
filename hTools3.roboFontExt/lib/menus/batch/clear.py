# menuTitle : clear data

from importlib import reload
import hTools3.dialogs.batch.clear
reload(hTools3.dialogs.batch.clear)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.batch.clear import BatchClearDialog

OpenWindow(BatchClearDialog)
