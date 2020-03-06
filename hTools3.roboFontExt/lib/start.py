import os
import sys

# add module
libFolder = os.getcwd()
print('\tadding hTools3 module to sys.path...')
sys.path.append(libFolder)

# add menu
from hTools3.modules.sys import add_hTools3_menu_main
print('initializing hTools3...\n')
add_hTools3_menu_main('menus', verbose=True)
# add_hTools3_menu_contextual_font(menusFolder, verbose=VERBOSE)
print('\n...done.\n')
