# coding: utf-8

'''Tools to work with fonts.'''

from __future__ import print_function

import os
import plistlib
from colorsys import hsv_to_rgb
from fontPens.penTools import distance
from mojo.roboFont import CurrentGlyph, CurrentFont, NewFont, RFont
from mojo.UI import getDefault
from hTools3.extras.fontAppTools import *

def getGlyphs(font):
    '''
    Return the current glyph selection in the font as a list of glyph names.

    - single window mode : currentGlyph AND fontSelection
    - multi- window mode : currentGlyph OR  fontSelection

    '''
    currentGlyph  = CurrentGlyph()
    fontSelection = font.selectedGlyphNames
    singleWindow  = [False, True][getDefault("singleWindowMode")]

    glyphNames = []

    if singleWindow:
        if currentGlyph is not None:
            glyphNames += [currentGlyph.name]
        glyphNames += fontSelection

    else:
        if len(fontSelection):
            glyphNames += fontSelection
        else:
            if currentGlyph is not None:
                glyphNames += [currentGlyph.name]

    # remove duplicates
    glyphNames_ = []
    for g in glyphNames:
        if g not in glyphNames_:
            glyphNames_.append(g)

    return glyphNames_

def getFontID(fontOrFontPath):
    '''
    Creates a unique font ID string in the format "familyName styleName (fontPath)".

    Args:
        fontOrFontPath (RFont or str): A font object or a path to a font file.

    Returns:
        A font ID string.

    '''

    # `fontOrFontPath` is an RFont object
    if isinstance(fontOrFontPath, RFont):
        font       = fontOrFontPath
        fontPath   = font.path
        familyName = font.info.familyName
        styleName  = font.info.styleName

    # `fontOrFontPath` is a UFO path
    elif isinstance(fontOrFontPath, str):
        fontPath      = fontOrFontPath
        infoPlistPath = os.path.join(fontPath, 'fontinfo.plist')

        with open(infoPlistPath, 'rb') as f:
            fontInfo = plistlib.load(f)

        familyName = fontInfo['familyName'] if 'familyName' in fontInfo else None
        styleName  = fontInfo['styleName']  if 'styleName'  in fontInfo else None

    # `fontOrPath` is neither a font objcect or a UFO path
    else:
        print('invalid font: %s\n' % fontOrFontPath)
        return

    # done!
    return "%s %s (%s)" % (familyName, styleName, fontPath)

def parseGString(font, gString):
    '''
    Convert an input string into a list of glyph names.

    Args:
        font (RFont): A font object.
        gString (str): A text input string.

    '''

    # build cmap
    cmap = dict(hyperCMAP(font))

    # reverse cmap
    cmap = {v: k for k, v in cmap.items()}
    glyphNames = splitText(gString, cmap)

    return glyphNames

#------------
# clear data
#------------

def clearUnicodes(font):
    '''
    Clear unicodes of all glyphs in the font.

    '''
    for g in font:
        if g.unicodes:
            g.unicodes = []
            if font.hasInterface():
                g.changed()

    if font.hasInterface():
        font.changed()

def clearAllGuidelines(font):
    '''
    Clear all font-level and glyph-level guidelines in the font.

    '''
    # clear font-level guides
    font.clearGuidelines()

    # clear glyph-level guides
    for g in font:
        g.clearGuidelines()
        if font.hasInterface():
            g.changed()

    if font.hasInterface():
        font.changed()

#-------------
# mark colors
#-------------

def markGlyphs(font, glyphNames, color, verbose=True):
    '''
    Set mark color for a list of glyph names in the font.

    Args:
        font (RFont): A font object.
        glyphNames (list): A list of glyph names.
        color (tuple or None): A mark color as a RGBA tuple or ``None``.

    '''
    if verbose:
        print('marking selected glyphs...\n')
        if color is None:
            print('\tcolor: (None)\n')
        else:
            print('\tcolor: %s, %s, %s, %s\n' % color)
        print('\t', end='')

    # mark glyphs
    for i, glyphName in enumerate(glyphNames):
        if verbose:
            if i == 0:
                print(glyphName, end='')
            else:
                print(', %s' % glyphName, end='')
        font[glyphName].markColor = color

        if font.hasInterface():
            font[glyphName].changed()

    # done
    if verbose:
        print('\n\n...done.\n')

    if font.hasInterface():
        font.changed()

def clearMarkColors(font):
    '''
    Clear all mark colors for all glyphs in the font.

    '''
    markGlyphs(font, font.keys(), None, verbose=False)

#-------------
# find glyphs
#-------------

def findMarkColor(font, color):
    '''
    Find all glyphs in the font with a given mark color.

    '''
    return [g.name for g in font if g.markColor == color]

def findContoursOnly(font):
    '''
    Find all glyphs in the font which contain only contours (no components).

    '''
    return [g.name for g in font if len(g.contours) and not len(g.components)]

def findComponentsOnly(font):
    '''
    Find all glyphs in the font which contain only components (no contours).

    '''
    return [g.name for g in font if not len(g.contours) and len(g.components)]

def findContoursAndComponents(font):
    '''
    Find all glyphs in the font which contain contours _and_ components.

    '''
    return [g.name for g in font if len(g.contours) and len(g.components)]

def findEmptyGlyphs(font):
    '''
    Find all glyphs in the font which contain neither contours nor components.

    '''
    return [g.name for g in font if not len(g.contours) and not len(g.components)]

def findOpenContours(font):
    '''
    Find all glyphs in the font which contain open contours.

    '''
    return [g.name for g in font for c in g.contours if c.open]

def findShortSegments(font, threshold=10):
    '''
    Find all glyphs in the font which contain a segment smaller than the given threshold value.

    '''
    glyphNames = []
    for glyphName in font.keys():
        for c in font[glyphName].contours:
            if glyphName in glyphNames:
                continue
            for i, bPoint in enumerate(c.bPoints):
                if i < len(c.bPoints) - 1:
                    bPointNext = c.bPoints[i+1]
                    pt1 = bPoint.anchor
                    pt2 = bPointNext.anchor
                    if not distance(pt1, pt2) < threshold:
                        continue
                    if glyphName in glyphNames:
                        continue
                    glyphNames.append(glyphName)
    return glyphNames

def findClosePoints(font, threshold=0):
    '''
    Find all glyphs in the font which contain points which are closer than the given threshold value.

    '''
    # not implemented yet
    return []

def findAttribute(font, attr, mark=True, sort=False, cluster=1):

    # collect values
    values = {}
    for glyphName in font.glyphOrder:
        g = font[glyphName]

        try:
            L = getattr(g, attr)
        except:
            continue

        # round value
        if cluster:
            L = int(L)

        if L not in values:
            values[L] = []
        values[L].append(g.name)

    if not len(values):
        return

    # process glyphs
    glyphOrder = []
    colorStep = 1.0 / (len(values) - 1)

    for i, L in enumerate(sorted(values)):
        if mark:
            hue = i * colorStep
            color = hsv_to_rgb(hue, 1, 1) + (0.5,)
        for glyphName in values[L]:
            glyphOrder.append(glyphName)
            # set mark color
            if mark:
                font[glyphName].markColor = color

    # set glyph order
    if sort:
        font.glyphOrder = glyphOrder

    # done
    return values

