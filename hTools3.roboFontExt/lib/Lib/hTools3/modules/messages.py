# coding: utf-8

'''
A collection of standard messages for use in hTools3 dialogs.

'''

def noXSelected(x):
    '''
    Generic message to be used when a required object is not selected.

    '''
    return 'No %s selected. Please select one or more %ss before using this dialog.\n' % (x, x)

def noXOpen(x):
    '''
    Generic message to be used when a required object is not open.

    '''
    return 'There is no %s window open. Please open at least one %s before using this dialog.\n' % (x, x)

# ------
# points
# ------

#: Message to be used when no point is selected.
noPointSelected = noXSelected('point')

#: Message to be used when only one point is selected.
onlyOnePoint = 'There is only one point selected. Please select at least two points before using this dialog.\n'

#: Message to be used when at least two points must be selected.
atLeastTwoPoints = 'Please select at least two points before using this dialog.\n'

# --------
# contours
# --------

#: Message to be used when no contour is selected.
noContourSelected = noXSelected('contour')

# ------
# glyphs
# ------

#: Message to be used when no glyph is open.
noGlyphOpen = noXOpen('glyph')

#: Message to be used when no glyph is selected.
noGlyphSelected = noXSelected('glyph')

# ------
# layers
# ------

#: Message to be used when no layer is selected.
noLayerSelected = noXSelected('layer')

# -----
# fonts
# -----

#: Message to be used when no font is open.
noFontOpen = noXOpen('font')

#: Message to be used when at least two fonts must be open.
onlyOneFont = 'There is only one font open. Please open at least one more font before using this dialog.\n'

# ------
# folder
# ------

#: Message to be used when there are no font files in a given folder.
noFontInFolder = 'There is no font in this folder. Please add some fonts to the folder, or choose another folder.\n'
