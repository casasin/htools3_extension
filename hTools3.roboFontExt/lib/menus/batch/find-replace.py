# menuTitle : find & replace

from importlib import reload
import hTools3.dialogs.batch.findReplace
reload(hTools3.dialogs.batch.findReplace)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.batch.findReplace import BatchFindReplaceDialog

OpenWindow(BatchFindReplaceDialog)
