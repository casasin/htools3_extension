from importlib import reload
import hTools3.modules.sys
reload(hTools3.modules.sys)

import os
import time
from xml.etree.ElementTree import parse
from fontTools.ttLib import TTFont
from hTools3.modules.sys import SuppressPrint

# functions

def ttx2otf(ttxPath, otfPath=None):
    '''
    Generate an .otf font from a .ttx file.

    **ttxPath** Path of the .ttx font source.
    **otfPath** Path of the target .otf font.

    '''
    # make otf path
    if not otfPath:
        otfPath = '%s.otf' % os.path.splitext(ttxPath)[0]
    # save otf font
    with SuppressPrint():
        tt = TTFont()
        tt.verbose = False
        tt.importXML(ttxPath)
        tt.save(otfPath)
        tt.close()

def otf2ttx(otfPath, ttxPath=None):
    '''
    Generate a .ttx font from an .otf file.

    **otfPath** Path of the .otf font source.
    **ttxPath** Path of the target .ttx font.

    '''
    # make ttx path
    if not ttxPath:
        ttxPath = '%s.ttx' % os.path.splitext(otfPath)[0]
    # save ttx font
    with SuppressPrint():
        tt = TTFont(otfPath)
        tt.verbose = False
        tt.saveXML(ttxPath)
        tt.close()

def stripNames(ttxPath):
    '''
    Clear several nameIDs to prevent the font from being installable on desktop OSs.

    **ttxPath** Path of the .ttx font to be modified.

    '''
    # nameIDs which will be erased
    nameIDs = [1, 2, 4, 16, 17, 18]
    tree = parse(ttxPath)
    root = tree.getroot()
    for child in root.find('name'):
        if int(child.attrib['nameID']) in nameIDs:
            child.text = ' '
    tree.write(ttxPath)

def setVersionString(ttxPath, text):
    tree = parse(ttxPath)
    root = tree.getroot()
    for child in root.find('name'):
        if child.attrib['nameID'] == '5':
            child.text = text
    tree.write(ttxPath)

def setUniqueName(ttxPath, uniqueName):
    tree = parse(ttxPath)
    root = tree.getroot()
    for child in root.find('name'):
        if child.attrib['nameID'] == '3':
            child.text = uniqueName
    tree.write(ttxPath)

def fixFontInfo(otfPath, familyName, styleName, versionMajor, versionMinor, ttxClear=True):
    ttxPath       = otfPath.replace('.otf', '.ttx')
    timestamp     = time.strftime("%Y%m%d.%H%M%S", time.localtime())
    versionString = 'Version %s.%s' % (versionMajor, versionMinor)
    uniqueName    = '%s %s: %s' % (familyName, styleName, timestamp)

    otf2ttx(otfPath, ttxPath)
    setVersionString(ttxPath, versionString)
    setUniqueName(ttxPath, uniqueName)
    ttx2otf(ttxPath, otfPath)

    if ttxClear:
        os.remove(ttxPath)

def makeDSIG(ttFont):
    '''
    Add a dummy DSIG table to an OpenType-TTF font, so positioning features work in Office applications on Windows.

    thanks to Ben Kiel on TypeDrawers:
    http://typedrawers.com/discussion/192/making-ot-ttf-layout-features-work-in-ms-word-2010

    '''
    from fontTools import ttLib
    from fontTools.ttLib.tables.D_S_I_G_ import SignatureRecord

    dsig = ttLib.newTable("DSIG")
    dsig.ulVersion = 1
    dsig.usFlag = 1
    dsig.usNumSigs = 1
    sig = SignatureRecord()
    sig.ulLength = 20
    sig.cbSignature = 12
    sig.usReserved2 = 0
    sig.usReserved1 = 0
    sig.pkcs7 = b'\xd3M4\xd3M5\xd3M4\xd3M4'
    sig.ulFormat = 1
    sig.ulOffset = 20
    dsig.signatureRecords = [sig]
    ttFont["DSIG"] = dsig
    # ugly but necessary -> so all tables are added to ttfont
    # ttFont.lazy = False
    # for key in ttFont.keys():
    #     print(ttFont[key])

def add_DSIG_table(otfPath):
    # with SuppressPrint():
    ttFont = TTFont(otfPath)
    makeDSIG(ttFont)
    ttFont.save(otfPath)
    ttFont.close()

def extractTables(otfPath, destFolder, tableNames=['name'], split=True):
    '''
    Extract font tables from an OpenType font as .ttx.

    '''
    ttfont = TTFont(otfPath)
    info_file = os.path.splitext(os.path.split(otfPath)[1])[0]
    info_path = os.path.join(destFolder, '%s.ttx' % info_file)
    ttfont.saveXML(info_path, tables=tableNames, splitTables=split)
    ttfont.close()

def findAndReplaceOTF(otfPath, destPath, findString, replaceString, tables=['name']):
    ttxPath = '%s.ttx' % os.path.splitext(otfPath)[0]
    otf2ttx(otfPath, ttxPath)
    findAndReplaceTTX(ttxPath, findString, replaceString, tables)
    ttx2otf(ttxPath, destPath)
    os.remove(ttxPath)

def clearDSIG(otfPath, verbose=True):
    ttFont = TTFont(otfPath)
    try:
        del ttFont["DSIG"]
        ttFont.save(otfPath)
    except:
        print("font does not have a 'DSIG' table")
    finally:
        ttFont.close()

def findAndReplaceTTX(ttxPath, findString, replaceString, tables=['name']):
    count = 0

    if 'name' in tables:
        tree  = parse(ttxPath)
        root  = tree.getroot()
        for child in root.find('name'):
            if child.text.find(findString) != -1:
                new_text = child.text.replace(findString, replaceString)
                child.text = new_text
                count += 1
        tree.write(ttxPath)

    if 'CFF ' in tables:
        CFF_elements = ['version', 'Notice', 'Copyright', 'FullName', 'FamilyName', 'Weight']
        ttFont = TTFont()
        ttFont.importXML(ttxPath)
        font_dict = ttFont['CFF '].cff.topDictIndex.items[0]
        for element in CFF_elements:
            text = getattr(font_dict, element)
            if text.find(findString) != -1:
                new_text = text.replace(findString, replaceString)
                setattr(font_dict, element, new_text)
                count += 1
        ttFont.saveXML(ttxPath)
        ttFont.close()

    return count
