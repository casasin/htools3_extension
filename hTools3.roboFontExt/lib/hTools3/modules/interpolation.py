# coding: utf-8

from mojo.tools import IntersectGlyphWithLine
from fontParts.fontshell import RGlyph

#---------------------
# low-level functions
#---------------------

def interpolateValues(value1, value2, factor):
    '''
    Interpolate between two values by a given factor.

    Args:
        value1 (int or float): A numerical value.
        value2 (int or float): Another numerical value.
        factor (float): The interpolation factor.

    >>> interpolateValues(20, 120, 0.5)
    70.0

    '''
    return value1 + (value2 - value1) * factor

def interpolateTuples(tuple1, tuple2, steps):
    '''
    Interpolate a given amount of steps between two tuples of arbitrary length.

    Args:
        tuple1 (tuple): A tuple of values.
        tuple2 (tuple): Another tuple of values.
        steps (int): The amount of interpolation steps.

    Returns:
        A list of interpolation steps between the two input tuples.

    >>> interpolateTuples((20, 50), (120, 100), 3))
    [(20.0, 50.0), (70.0, 75.0), (120.0, 100.0)]

    '''
    tuplesResult = []
    for i in range(steps):
        factor = i * (1.0 / (steps - 1))
        tuple3 = []
        for j, v1 in enumerate(tuple1):
            v2 = tuple2[j]
            v3 = interpolateValues(v1, v2, factor)
            tuple3.append(v3)
        tuplesResult.append(tuple(tuple3))
    return tuplesResult

def calculateFactorLinear(steps, step):
    return i / (steps - 1)

#---------------
# stem formulas
#---------------

def calculateStemLinear(v1, v2, steps, step):
    return v1 + (v2 - v1) / (steps - 1) * (step - 1)

def calculateStemLucas(v1, v2, steps, step):
    return v1 * (v2 / v1) ** ((step - 1) / (steps - 1))

def getStem(glyph, beamY):
    '''
    Get the horizontal stem width of a glyph at a given y position.

    Args:
        glyph (RGlyph): A glyph object.
        beamY (int or float): The y position of the horizontal measuring beam.

    Returns:
        The horizontal stem width of the glyph as a float or integer.

    >>> g = CurrentGlyph()
    >>> getStem(g, 200)
    95

    '''
    line = (-10000, beamY), (10000, beamY)
    pts = IntersectGlyphWithLine(glyph, line, canHaveComponent=True, addSideBearings=False)
    pts = sorted([int(round(pt[0])) for pt in pts])
    return pts[1] - pts[0]

def getStemFactor(stem, g1, g2, beamY=200, tolerance=5, increment=0.001, verbose=False, cycles=10000):

    # TODO: implement tolerance value

    if not g1.isCompatible(g2):
        return

    i = increment
    t = tolerance

    n = 0
    while n <= cycles:

        # make temp factor incrementally
        factor = i * n

        # make temp glyph
        g3 = RGlyph()
        g3.interpolate(factor, g1, g2)

        # get temp stem
        tmpStem = getStem(g3, beamY)

        # print cycle info
        if verbose:
            print("%02i" % n, '%.3f' % factor, tmpStem, stem, tmpStem < stem, tmpStem == stem, tmpStem > stem)

        # found matching factor for stem
        if tmpStem == stem:
            return factor

        # passed matching factor for stem;
        # invert & reduce scale to go back
        elif tmpStem > stem:
            i *= -0.1

        # matching factor is ahead;
        # continue at the same rate
        else:
            i = abs(i)

        # advance to next cycle
        n += 1

#------------
# glyph math
#------------

def interpolateGlyphsLinear(g1, g2, steps, step):
    return g1 + (g2 - g1) / (steps - 1) * (step - 1)

def interpolateGlyphsLucas(g1, g2, steps, step, beamY=200):
    stem1 = getStem(g1, beamY)
    stem2 = getStem(g2, beamY)
    stems = [calculateStemLucas(stem1, stem2, steps, i+1) for i in range(steps)]
    factors = [getStemFactor(int(stem), g1, g2, tolerance=0, increment=0.001, cycles=10000) for stem in stems]
    g = RGlyph()
    g.interpolate(factors[step], g1, g2)
    return g

#---------------------
# glyph interpolation
#---------------------

def condenseGlyph(glyph1, glyph2, glyph3, stem1, stem2, factor):
    '''
    Generate a condensed glyph by interpolating between a regular and a bold glyph.

    Args:
        glyph1 (RGlyph): A regular glyph.
        glyph2 (RGlyph): A bold glyph.
        glyph3 (RGlyph): A glyph for the resulting condesed glyph.
        stem1 (int or float): The stem width of the regular font.
        stem2 (int or float): The stem width of the bold font.
        factor (float): The interpolation factor.

    .. code-block:: python

        f1 = AllFonts().getFontsByStyleName('Roman')[0]
        f2 = AllFonts().getFontsByStyleName('Bold')[0]
        f3 = NewFont()
        g3 = f3.newGlyph('a')
        condenseGlyph(f1['a'], f2['a'], g3, 95, 143, 0.5)

    '''
    # calculate horizontal scale
    scaleX = float(stem1) / (stem1 + factor * (stem2 - stem1))

    # interpolate masters
    glyph3.interpolate((factor, 0), glyph1, glyph2)

    # scale horizontally
    glyph3.scaleBy((scaleX, 1))

    # calculate margins
    if not glyph1.bounds or not glyph2.bounds:
        return

    glyph3.leftMargin  = (glyph1.leftMargin  + glyph2.leftMargin)  * 0.5 * (1.0 - factor)
    glyph3.rightMargin = (glyph1.rightMargin + glyph2.rightMargin) * 0.5 * (1.0 - factor)

def condenseGlyphs(font1, font2, font3, stem1, stem2, factor, glyphNames):
    '''
    Generate condensed glyphs by interpolating between regular and bold fonts.

    Args:
        font1 (RGlyph): A regular font.
        font2 (RGlyph): A bold font.
        font3 (RGlyph): A condesed font for the resulting glyphs.
        stem1 (int or float): The stem width of the regular font.
        stem2 (int or float): The stem width of the bold font.
        factor (float): The interpolation factor.
        glyphNames (list): A list of glyph names to condense.

    .. code-block:: python

        f1 = AllFonts().getFontsByStyleName('Roman')[0]
        f2 = AllFonts().getFontsByStyleName('Bold')[0]
        f3 = NewFont()
        condenseGlyphs(f1, f2, f3, 95, 143, 0.5, list('abcd'))

    '''
    # calculate horizontal scale
    scaleX = float(stem1) / (stem1 + factor * (stem2 - stem1))

    # interpolate and scale glyphs
    for glyphName in glyphNames:

        # create glyph in destination font
        if glyphName not in font3:
            font3.newGlyph(glyphName)

        # get glyphs from glyph name
        g1, g2, g3 = font1[glyphName], font2[glyphName], font3[glyphName]

        # interpolate and scale
        g3.prepareUndo('condensomatic')
        g3.interpolate((factor, 0), g1, g2)
        g3.scaleBy((scaleX, 1))

        # calculate margins
        if g1.bounds and g2.bounds:
            g3.leftMargin  = (g1.leftMargin  + g2.leftMargin)  * 0.5 * (1.0 - factor)
            g3.rightMargin = (g1.rightMargin + g2.rightMargin) * 0.5 * (1.0 - factor)

        # done with glyph
        g3.changed()
        g3.performUndo()

    # done
    font3.changed()

def interpolateStepsInFont(font, g1, g2, interSteps, extraSteps, prefix='result', mark=False, verbose=True, mode='linear'):
    '''
    Interpolate a range of steps between two glyphs in the same font.

    Args:
        font (RFont): A font object.
        g1 (RGlyph): A master glyph.
        g2 (RGlyph): Another master glyph.
        interSteps (int): The amount of interpolation steps.
        extraSteps (int): The amount of extrapolation steps.
        prefix (str): A prefix for the glyph names of the resulting glyphs.
        mark (bool): Mark the resulting glyphs and the master glyphs with different colors.

    .. code-block:: python

        f = CurrentFont()
        g1 = f['o']
        g2 = f['O']
        interpolateStepsInFont(f, g1, g2, 6, 2, prefix='result', mark=True)

    '''
    steps = range(-extraSteps, interSteps + extraSteps + 2)
    glyphNames = ["%s.%03i" % (prefix, i) for i in range(len(steps))]

    if mode == 'lucas':
        glyphs = [interpolateGlyphsLucas(g1, g2, interSteps+1, step) for step in steps]
    else:
        glyphs = [interpolateGlyphsLinear(g1, g2, interSteps+1, step) for step in steps]

    roles = [0 if (step == 0 or step == interSteps+1) else 2 if (step < 0 or step > interSteps+1) else 1 for step in steps]
    roleColors = [(1, 0, 0, 0.5), (0, 1, 0, 0.5), (0, 0, 1, 0.5)]
    roleNames = ['master', 'interpolation', 'extrapolation']

    for i, step in enumerate(steps):
        font.insertGlyph(glyphs[i], name=glyphNames[i])
        if mark:
            font[glyphNames[i]].markColor = roleColors[roles[i]]
        if verbose:
            print("%02i" % i, glyphNames[i], "%+03i" % step, roleNames[roles[i]])

    font.changed()

def interpolateGlyphsInFont(font, glyphName1, glyphName2, factors, prefix='result', verbose=True):
    '''
    Interpolate a range of steps between two glyphs in the same font using a given list of factors.

    Args:
        font (RFont): A font object.
        glyphName1 (RGlyph): A master glyph.
        glyphName2 (RGlyph): Another master glyph.
        interSteps (int): The amount of interpolation steps.
        extraSteps (int): The amount of extrapolation steps.
        prefix (str): A prefix for the glyph names of the resulting glyphs.
        mark (bool): Mark the resulting glyphs and the master glyphs with different colors.

    '''
    # no font open
    if font is None:
        if verbose:
            print("no font open")
        return

    # make sure the font contains both glyphs
    if not glyphName1 in font:
        if verbose:
            print("font does not contain a glyph named '%s'" % glyphName1)
        return

    if not glyphName2 in font:
        if verbose:
            print("font does not contain a glyph named '%s'" % glyphName2)
        return

    # get the two master glyphs
    glyph1 = font[glyphName1]
    glyph2 = font[glyphName2]

    # make sure the two glyphs are compatible
    if not glyph1.isCompatible(glyph2)[0]:
        if verbose:
            print("Glyphs %s and %s are not compatible." % (glyph.name, glyph2.name))
        return

    for i, factor in enumerate(factors):

        # create glyph name
        resultName = "%s.%03i" % (prefix, i)

        # create glyph if it does not yet exist
        glyph3 = font.newGlyph(resultName)

        # interpolate master glyphs with factor
        glyph3.interpolate(factor, glyph1, glyph2)

    # done!
    font.changed()