import os
import sys

def add_hTools3_module(verbose=False):
    libFolder = os.getcwd()
    if verbose:
        print('\tadding hTools3 module...')
    sys.path.append(libFolder)

def add_hTools3_menu(folderName, verbose=False):
    from hTools3.modules.sys import addMenu
    folderName = os.path.join(os.getcwd(), folderName)
    if verbose:
        print('\tadding hTools3 menu...')
    addMenu('hTools3', folderName)

# --------
# settings
# --------

VERBOSE = True
DEVMODE = False

# ----------
# initialize
# ----------

menusFolder = 'menus' if not DEVMODE else 'menus_dev'

print('initializing hTools3...\n')
add_hTools3_module(verbose=VERBOSE)
add_hTools3_menu(menusFolder, verbose=VERBOSE)
print('\n...done.\n')
