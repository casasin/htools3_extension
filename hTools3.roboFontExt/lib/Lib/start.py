import os
import sys

def add_hTools3_module(verbose=False):
    libFolder = os.getcwd()
    if verbose:
        print('\tadding hTools3 module to sys.path...')
    sys.path.append(libFolder)

def add_hTools3_menu_main(folderName, verbose=False):
    from hTools3.modules.sys import addMenu
    folderName = os.path.join(os.getcwd(), folderName)
    if verbose:
        print('\tadding hTools3 to the main application menu...')
    addMenu('hTools3', folderName)

def add_hTools3_menu_contextual_font(folderName, verbose=False):
    if verbose:
        print('\tadding hTools3 to the Font Overview contextual menu...')
    pass

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
add_hTools3_menu_main(menusFolder, verbose=VERBOSE)
# add_hTools3_menu_contextual_font(menusFolder, verbose=VERBOSE)
print('\n...done.\n')
