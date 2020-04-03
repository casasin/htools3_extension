# menuTitle : set data

from importlib import reload
import hTools3.dialogs.batch.set
reload(hTools3.dialogs.batch.set)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.batch.set import BatchSetDialog

OpenWindow(BatchSetDialog)
