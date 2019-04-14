# coding: utf-8

'''Tools to work with glyphs.'''

# def clearOutlines(glyph):
#     pass

# def decompose(glyph):
#     pass

# def autoContourOrder(glyph):
#     pass

# def autoContourDirection(glyph):
#     pass

# def autoStartingPoints(glyph):
#     pass

# def removeOverlap(glyph):
#     pass

# def addExtremePoints(g):
#     pass

def getOriginPosition(glyph, posName):
    '''
    Get a position based on the glyph bounds and a named reference point.

    Args:
        glyph (RGlyph): A glyph object.
        posName (str): The name of a reference point.

    Returns:
        A position as a tuple of (x,y) values.

    .. code-block:: python

        >>> getOriginPosition(CurrentGlyph(), 'middleCenter')
        (243.5, 237.5)

    '''
    if not glyph.bounds:
        return
    left, bottom, right, top = glyph.bounds
    center = left   + (right - left)   * 0.5
    middle = bottom + (top   - bottom) * 0.5
    positions = {
        'topLeft'      : (left,   top),
        'topCenter'    : (center, top),
        'topRight'     : (right,  top),
        'middleLeft'   : (left,   middle),
        'middleCenter' : (center, middle),
        'middleRight'  : (right,  middle),
        'bottomLeft'   : (left,   bottom),
        'bottomCenter' : (center, bottom),
        'bottomRight'  : (right,  bottom),
    }
    if posName not in positions:
        return
    return positions[posName]

def deselectPoints(glyph):
    '''
    Deselect all points in a glyph.

    '''
    for c in glyph.contours:
        for p in c.points:
            p.selected = False

def selectPointsLine(glyph, pos, axis='x', side=0):
    '''
    Select all points below/above a given position.

    Args:
        glyph (RGlyph): A glyph object.
        pos (int or float): The position of an imaginary line.
        axis (str): The selection axis perpendicular to the line. (*x* or *y*)
        side (int): The side of the selection in relation to the line. (``0``: smaller or ``1``: greater)

    '''
    for c in glyph.contours:
        for p in c.points:
            value = p.x if axis == 'x' else p.y
            if not side:
                if value <= pos:
                    p.selected = True
            else:
                if value >= pos:
                    p.selected = True

def shiftSelectedPoints(glyph, delta, axis='x'):
    '''
    Shift all selected points along one axis by a given amount of units.

    Args:
        glyph (RGlyph): A glyph object.
        delta (int or float): The distance to move the selected points.
        axis (str): The axis along which to move the selected points.

    .. code-block:: python

        g = CurrentGlyph()
        g.prepareUndo('shift points')
        deselectPoints(g)
        selectPointsLine(g, 200, axis='y', side=0)
        shiftSelectedPoints(g, -100, axis='y')
        g.changed()
        g.performUndo()

    '''
    for c in glyph.contours:
        for p in c.selectedPoints:
            if axis == 'x':
                p.x += delta
            else:
                p.y += delta

# --------
# rounding
# --------

def roundPoints(glyph, gridSize):
    '''
    Round all point positions to a given grid.

    '''
    for contour in glyph.contours:
        for pt in contour.points:
            pt.x = round(pt.x / gridSize) * gridSize
            pt.y = round(pt.y / gridSize) * gridSize

def roundBPoints(glyph, gridSize):
    '''
    Round all bPoint positions to a given grid.

    '''
    for contour in glyph.contours:
        for bPoint in contour.bPoints:
            x, y = bPoint.anchor
            x = round(x / gridSize) * gridSize
            y = round(y / gridSize) * gridSize
            bPoint.anchor = x, y

def roundAnchors(glyph, gridSize):
    '''
    Round all anchor positions to a given grid.

    '''
    for anchor in glyph.anchors:
        anchor.x = round(anchor.x / gridSize) * gridSize
        anchor.y = round(anchor.y / gridSize) * gridSize

def roundComponents(glyph, gridSize):
    '''
    Round all components positions to a given grid.

    '''
    for component in glyph.components:
        x, y = component.offset
        x = round(x / gridSize) * gridSize
        y = round(y / gridSize) * gridSize
        component.offset = x, y

def roundMargins(glyph, gridSize):
    '''
    Round the margins of a glyph to a given grid.

    '''
    if glyph.bounds is None:
        return
    L, B, R, T  = glyph.bounds
    leftMargin  = round(glyph.leftMargin / gridSize) * gridSize
    rightMargin = round(glyph.rightMargin / gridSize) * gridSize
    width = leftMargin + (R - L) + rightMargin
    glyph.leftMargin = leftMargin
    glyph.width = width

def roundWidth(glyph, gridSize):
    '''
    Round the width of a glyph to a given grid.

    '''
    glyph.width = round(glyph.width / gridSize) * gridSize

# ------
# suffix
# ------

def hasSuffix(glyph, suffix):
    '''
    Check if a glyph's name has a given ``suffix``.

    '''
    hasSuffix = False
    nameParts = glyph.name.split(".")

    # check for suffix
    if len(nameParts) == 2:
        if nameParts[1] == suffix:
            hasSuffix = True

    # check for no suffix
    else:
        if len(nameParts) == 1 and len(suffix) == 0:
            hasSuffix = True

    return hasSuffix

def changeSuffix(glyph, oldSuffix, newSuffix=None):
    '''
    Create a new glyph name with a different suffix.

    Args:
        glyph (RGlyph): A glyph object.
        oldSuffix (str): The old suffix to be replaced.
        newSuffix (str or None): The new suffix to be used in place of the old one.

    Returns:
        A new glyph name with a modified or removed suffix.

    '''
    baseName = glyph.name.split(".")[0]

    # replace suffix
    if newSuffix is not None:
        newName = "%s.%s" % (baseName, newSuffix)

    # clear suffix
    else:
        newName = baseName

    return newName

def renameGlyphSuffix(glyph, oldSuffix, newSuffix, overwrite=False, duplicate=False, verbose=True):
    '''
    Add, remove or modify a glyph name’s suffix.

    Args:
        glyph (RGlyph): A glyph object.
        oldSuffix (str): The old suffix to be replaced.
        newSuffix (str or None): The new suffix to be used in place of the old one.
        overwrite (bool): If a glyph with the new name already exist in the parent font, overwrite it (or not).
        duplicate (bool): Keep the original glyph with the old suffix name.

    '''

    # glyph does not have suffix
    if not hasSuffix(glyph, oldSuffix):
        return

    # switch suffixes : one.osf -> one.onum
    if len(oldSuffix) > 0 and len(newSuffix) > 0:
        newName = changeSuffix(glyph, oldSuffix, newSuffix)

    # remove suffix : one.osf -> one
    elif len(oldSuffix) > 0 and len(newSuffix) == 0:
        newName = changeSuffix(glyph, oldSuffix, None)

    # add suffix : one -> one.onum
    elif len(oldSuffix) == 0 and len(newSuffix) > 0:
        newName = '%s.%s' % (glyph.name, newSuffix)

    # don't change glyph name
    else:
        newName = glyph.name
        return

    # get font
    font = glyph.font
    if font is None:
        return

    # rename glyph
    if newName != glyph.name:

        if newName in font:

            # don't overwrite existing glyph
            if not overwrite:
                print("\t'%s' already exists in font, skipping..." % newName)
                return

            # delete existing glyph (=overwrite)
            print("\tdeleting '%s'..." % newName)
            font.removeGlyph(newName)
            font.changed()

        # rename
        if not duplicate:
            if verbose:
                print("\trenaming '%s' as '%s'..." % (glyph.name, newName))
            glyph.name = newName
            glyph.changed()

        # rename as duplicate
        else:
            if verbose:
                print("\tduplicating '%s' as '%s'..." % (glyph.name, newName))
            font.insertGlyph(glyph, name=newName)
            font.changed()

# -------
# metrics
# -------

def setGlyphWidth(glyph, widthValue, positionMode):
    '''
    Transform the width of a glyph.

    Args:
        glyph (RGlyph): A glyph object.
        widthValue (int): A value to be used as input in the width modification.
        positionMode (int): The index of the position mode.

    0. do not move
    1. center glyph
    2. split margins
    3. relative split

    '''

    widthNew = widthValue
    leftOld  = glyph.leftMargin
    rightOld = glyph.rightMargin
    widthOld = glyph.width
    boxWidth = glyph.width - (glyph.leftMargin + glyph.rightMargin)

    # center glyph
    if positionMode == 'center glyph':
        glyph.width = widthNew
        centerGlyph(glyph)

    # split difference
    elif positionMode == 'split margins':
        try:
            diff = widthNew - widthOld
            leftNew = leftOld + (diff * 0.5)
        except:
            leftNew = 0
        glyph.leftMargin = leftNew
        glyph.width = widthNew

    # split relative
    elif positionMode == 'relative split':
        try:
            whitespace = widthNew - boxWidth
            leftNew = whitespace / (1 + (rightOld / leftOld))
        except:
            leftNew = 0
        glyph.leftMargin = leftNew
        glyph.width = widthNew

    # do not move
    else:
        glyph.width = widthNew

def centerGlyph(glyph):
    '''
    Center the glyph inside its advance width.

    '''
    if glyph.bounds is None:
        return

    whitespace = glyph.leftMargin + glyph.rightMargin
    width = glyph.width
    glyph.prepareUndo('center glyph')
    glyph.leftMargin = whitespace * 0.5
    glyph.width = width
    glyph.performUndo()

# ------
# points
# ------

def getPointFromBPoint(bPoint):
    '''
    Get a Point for a given bPoint.

    '''
    return bPoint._point

def getBPointFromPoint(point):
    '''
    Get a bPoint for a given point.

    '''
    from fontParts.fontshell import RBPoint

    bPoint = RBPoint()
    bPoint._setPoint(point)
    bPoint.contour = point.contour

    return bPoint

