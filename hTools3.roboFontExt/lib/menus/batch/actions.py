# menuTitle : actions

from importlib import reload
import hTools3.dialogs.batch.actions
reload(hTools3.dialogs.batch.actions)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.batch.actions import BatchActionsDialog

OpenWindow(BatchActionsDialog)
