# menuTitle : copy data

from importlib import reload
import hTools3.dialogs.batch.copy
reload(hTools3.dialogs.batch.copy)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.batch.copy import BatchCopyDialog

OpenWindow(BatchCopyDialog)
