# coding: utf-8

import os
import shutil
from mojo.roboFont import RFont, OpenFont
from fontTools.designspaceLib import DesignSpaceDocument


'''
Tools to create variable fonts. Early days, not much to see here…

'''

def buildVariableFontMasters(srcFolder, dstFolder, glyphOrder, fontInfoDict):

    '''
    Export UFO masters for generating variable fonts from multilayer complete design masters.

    - Layers in design masters are exported as separated UFOs for variable fonts.
    - To avoid errors during development, the glyph set is reduced based on the given glyph order.

    '''

    # remove existing var masters
    varUFOs = [os.path.join(dstFolder, f) for f in os.listdir(dstFolder) if os.path.splitext(f)[-1] == '.ufo']
    if varUFOs:
        for ufo in varUFOs:
            shutil.rmtree(ufo)

    # make var masters
    ufos = [os.path.join(srcFolder, f) for f in os.listdir(srcFolder) if os.path.splitext(f)[-1] == '.ufo']
    for ufo in ufos:
        f = OpenFont(ufo, showInterface=False)
        f.clearGuidelines()

        for layerName in f.layerOrder:
            if layerName in ['foreground', 'background']:
                continue

            layer = f.getLayer(layerName) # .copy()
            for glyph in layer:
                if glyph.name not in glyphOrder:
                    layer.removeGlyph(glyph.name)
                else:
                    glyph.clearGuidelines()

            f2 = RFont(showInterface=False)
            attrs = ['xHeight', 'capHeight', 'descender', 'ascender', 'unitsPerEm']
            for attr in attrs:
                setattr(f2.info, attr, getattr(f.info, attr))

            for attr, value in fontInfoDict.items():
                setattr(f2.info, attr, value)

            f2.info.styleName = layer.name
            f2.insertLayer(layer, name='foreground')
            f2.glyphOrder = glyphOrder

            ufoVarPath = os.path.join(dstFolder, f'{layerName}.ufo')
            f2.save(ufoVarPath)
            f2.close()

        # don't save!
        f.close()


def setVariableFontInfo(designSpacePath, fontInfoDict):
    '''
    Font info data specific to the variable font is set in the neutral master.

    '''
    designSpace = DesignSpaceDocument()
    designSpace.read(designSpacePath)
    varFolder = os.path.dirname(designSpacePath)
    neutralPath = os.path.join(varFolder, designSpace.default.filename)

    # set attributes in neutral master
    font = OpenFont(neutralPath, showInterface=False)
    for attr, value in fontInfoDict.items():
        setattr(font.info, attr, value)
    font.save()
