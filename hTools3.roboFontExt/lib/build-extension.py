from importlib import reload
import hTools3.modules.sys
reload(hTools3.modules.sys)

import os
import shutil
from mojo.extensions import ExtensionBundle
from hTools3.modules.sys import pycClear, removeGitFiles

# --------
# settings
# --------

version         = '0.3'
libFolder       = '/_code/hTools3_core'

baseFolder      = os.path.dirname(__file__)
licensePath     = os.path.join(baseFolder, 'license.txt')
resourcesFolder = os.path.join(baseFolder, 'resources')
imagePath       = os.path.join(resourcesFolder, 'icon.png')
docsFolder      = os.path.join(baseFolder, 'docs')
docsBuildFolder = os.path.join(docsFolder, 'build')
htmlFolder      = os.path.join(docsBuildFolder, 'html')

outputFolder    = '/_code/hTools3_core.extension'
extensionPath   = os.path.join(outputFolder, 'hTools3.roboFontExt')
pycOnly         = False # menus not working if pycOnly=True !!!

# ---------------
# build extension
# ---------------

def buildExtension():

    B = ExtensionBundle()
    B.name                 = "hTools3"
    B.developer            = 'Gustavo Ferreira'
    B.developerURL         = 'http://hipertipo.com/'
    B.icon                 = imagePath
    B.version              = version
    B.launchAtStartUp      = True
    B.mainScript           = 'Lib/start.py'
    B.uninstallScript      = ''
    B.html                 = True
    B.requiresVersionMajor = '3'
    B.requiresVersionMinor = '2'
    B.addToMenu            = [
        {
            'path'          : 'Lib/hTools3/dialogs/preferences.py',
            'preferredName' : 'preferences',
            'shortKey'      : '',
        },
    ]
    with open(licensePath) as license:
        B.license = license.read()

    if os.path.exists(extensionPath):
        shutil.rmtree(extensionPath)

    print('\tbuilding .roboFontExt package...')
    B.save(extensionPath, libPath=libFolder, htmlPath=htmlFolder, resourcesPath=resourcesFolder, pycOnly=pycOnly)

    errors = B.validationErrors()
    if len(errors):
        print(errors)

# ---------------
# build extension
# ---------------

pycClear(baseFolder)

print('building hTools3 %s...\n' % version)
buildExtension()
print('\n...done!\n')

removeGitFiles(extensionPath, verbose=True)
