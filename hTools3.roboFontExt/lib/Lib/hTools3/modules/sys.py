# coding: utf-8

import os
import subprocess
import shutil

try:
    from AppKit import NSApp, NSMenu, NSMenuItem
    from mojo.UI import setScriptingMenuNamingShortKeyForPath, createModifier
    try:
        from lib.UI.fileBrowser import RFPathItem
    except:
        from lib.UI.fileBrowser import PathItem as RFPathItem

# not in RoboFont
except:
    pass

def addMenu(name, path):
    '''
    Creates a new menu in RoboFont's main application menu.

    .. code-block:: python

        menuFolder = 'path/to/menuFolder'
        addMenu('myMenu', menuFolder)

    '''
    # create a new menu
    menu = NSMenu.alloc().initWithTitle_(name)

    # create a path item that will build the menu and connect all the callbacks
    pathItem = RFPathItem(path, ['.py'], isRoot=True)
    pathItem.getMenu(title=name, parentMenu=menu)

    # get the main menu
    menubar = NSApp().mainMenu()

    # search if the menu item already exists
    newItem = menubar.itemWithTitle_(name)
    if not newItem:
        # if not, create one and append it before `Help`
        newItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(name, '', '')
        menubar.insertItem_atIndex_(newItem, menubar.numberOfItems()-1)

    # set the menu as submenu
    newItem.setSubmenu_(menu)

# def addShortcuts(scriptsFolder, shortcuts, verbose=False):
#     '''
#     Creates keyboard shortcuts for scripts.

#     '''
#     for shortcut in shortcuts:
#         shortKey, name, scriptFile = shortcut
#         scriptPath = os.path.join(scriptsFolder, scriptFile)
#         modifier = createModifier(command=True, shift=True)
#         if os.path.exists(scriptPath):
#             if verbose:
#                 print('creating shortcut for', scriptPath)
#             setScriptingMenuNamingShortKeyForPath(scriptPath, name, shortKey, modifier)

def pycClear(folder, verbose=True):
    '''
    Recursively remove all .pyc files inside a folder.

    .. code-block:: python

        folder = 'path/to/folder'
        pycClear(folder)

    '''
    for fileName in os.listdir(folder):
        filePath = os.path.join(folder, fileName)
        if os.path.splitext(fileName)[-1] == '.pyc':
            if verbose:
                print('deleting %s...' % filePath)
            os.remove(filePath)
        elif os.path.isdir(filePath):
            pycClear(filePath)

def pyCacheClear(folder, verbose=True):
    '''
    Recursively remove all __pycache__ folders inside a folder.

    .. code-block:: python

        folder = 'path/to/folder'
        pyCacheClear(folder)

    '''

    for fileName in os.listdir(folder):
        filePath = os.path.join(folder, fileName)
        if fileName == '__pycache__':
            shutil.rmtree(filePath)
        elif os.path.isdir(filePath):
            pyCacheClear(filePath)

def openPDF(pdfPath):
    '''
    Open a PDF file in macOS Preview app.

    .. code-block:: python

        pdfPath = '/path/to/folder/test.pdf'
        openPDF(pdfPath)

    '''
    subprocess.call(['open', '-a', 'Preview', pdfPath])

def removeGitFiles(extensionPath, verbose=False):

    libFolder = os.path.join(extensionPath, 'Lib')
    folder, extensionFile = os.path.split(extensionPath)

    if verbose:
        print('removing git files from %s...\n' % extensionFile)

    if not os.path.exists(libFolder):
        print("\t('Lib' folder does not exist) %s" % libFolder)
        return

    # remove .git repository
    gitPath = os.path.join(libFolder, '.git')
    if not os.path.exists(gitPath):
        if verbose:
            print('\t(.git file does not exist) %s' % gitPath)
        return

    if verbose:
        print('\tremoving .git data... %s' % gitPath)
    shutil.rmtree(gitPath)

    # remove gitignore file
    gitignorePath = os.path.join(libFolder, '.gitignore')
    if os.path.exists(gitignorePath):
        if verbose:
            print('\tremoving .gitignore file... %s' % gitignorePath)
        os.remove(gitignorePath)

    if verbose:
        print('\n...done.\n')
