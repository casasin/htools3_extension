import os
import sys

'''
Clear all .pyc files and __pycache__ folders from a folder.

'''

try:
    import hTools3

except ModuleNotFoundError:
    libFolder = os.getcwd()
    sys.path.append(libFolder)
    import hTools3

from hTools3.modules.sys import pycClear, pyCacheClear

folder = os.path.dirname(hTools3.__path__[0])

pycClear(folder)
pyCacheClear(folder)
