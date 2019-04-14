# coding: utf-8

'''
Tools to work with accented glyphs using `Glyph Construction`_ syntax.

.. _Glyph Construction: https://github.com/typemytype/GlyphConstruction

'''

try:
    from glyphConstruction import *

except:
    print('glyphConstruction module is not installed.\n')
    pass

#: A basic default list of accent glyphs.
ACCENTS = ['acute', 'grave', 'circumflex', 'dieresis', 'tilde', 'macron', 'breve', 'dotaccent', 'ring', 'cedilla', 'hungarumlaut', 'ogonek', 'caron']

def buildGlyphConstructions(font, glyphConstructions, clear=True, markColor=None, verbose=False, indentLevel=0):
    r'''
    Build new glyphs in a font from a string of Glyph Construction definitions.

    Args:
        font (RFont): A font object.
        glyphConstructions (str): A string of Glyph Construction definitions, one per line.
        clear (bool): Clear glyph contents before constructing new glyph.
        markColor (tuple): Optional mark color for the constructed glyphs.
        verbose (bool): Turn text output on/off.
        indentLevel (int): Amount of whitespace to use before lines of text output.

    Returns:
        A list with the names of all glyphs built.

    >>> f = CurrentFont()
    >>> constructions = """\
    ... agrave = a + grave@center,`top+100`
    ... aacute = a + acute@center,`top+100`
    ... """
    >>> buildGlyphConstructions(f, constructions, verbose=True, indentLevel=0, markColor=(0, 1, 1, 0.5), clear=True)

    '''
    builtGlyphs = []

    # parse glyph construction text
    constructions = ParseGlyphConstructionListFromString(glyphConstructions)

    # build new glyphs
    for construction in constructions:

        # make construction glyph
        constructionGlyph = GlyphConstructionBuilder(construction, font)

        # print info
        if verbose:
            print('%sbuilding %s...' % ('\t' * indentLevel, constructionGlyph.name))

        # create new glyph in the font
        if constructionGlyph.name not in font:
            glyph = font.newGlyph(constructionGlyph.name)
        else:
            glyph = font[constructionGlyph.name]

        # clear target glyph contents
        if clear:
            glyph.clear()

        # copy construction glyph data to new glyph
        constructionGlyph.draw(glyph.getPen())

        # copy glyph attributes
        glyph.name    = constructionGlyph.name
        glyph.unicode = constructionGlyph.unicode
        glyph.note    = constructionGlyph.note
        glyph.width   = constructionGlyph.width

        # set mark color
        if markColor:
            glyph.markColor = markColor

        # done with glyph
        glyph.changed()
        builtGlyphs.append(glyph.name)

    return builtGlyphs

def extractGlyphConstructions(font, glyphNames=None, accents=ACCENTS):
    '''
    Extract Glyph Construction rules for selected composed glyphs.

    Args:
        font (RFont): A font object.
        glyphNames (list): A list with names of glyphs from which to extract glyph constructions.
        accents (list): A list with names of glyphs which are not base glyphs. *(optional)*

    Returns:
        A string of Glyph Construction definitions, one per line.

    >>> f = CurrentFont()
    >>> constructions = extractGlyphConstructions(f, glyphNames=['agrave', 'aacute'])
    >>> print(constructions)
    agrave = a + grave
    aacute = a + acute

    .. note:: The extracted glyph construction definitions are very basic. You’ll probably want to refine them with positioning instructions. See the `Glyph Construction`_ documentation for syntax examples.

    '''
    # get selected glyph names
    if not glyphNames:
        glyphNames = font.glyphOrder

    # collect extracted constructions
    constructions = []
    for glyphName in glyphNames:
        g = font[glyphName]
        if not len(g.components):
            continue
        constructions.append(extractGlyphConstruction(g, accents))

    # join constructions as multi-line string
    return '\n'.join(constructions)

def extractGlyphConstruction(glyph, accents=ACCENTS):
    '''
    Extract Glyph Construction rule from a glyph with components.

    Args:
        glyph (RGlyph): A glyph object.
        accents (list): A list with names of glyphs which are not base glyphs. *(optional)*

    Returns:
        A string of Glyph Construction definitions, one per line.

    >>> g = CurrentGlyph()
    >>> construction = extractGlyphConstruction(g)
    >>> print(construction)
    agrave = a + grave

    '''

    # collect base glyphs & accents separately
    baseGlyphs = []
    accentGlyphs = []
    for c in glyph.components:
        if c.baseGlyph in accents:
            accentGlyphs.append(c.baseGlyph)
        else:
            baseGlyphs.append(c.baseGlyph)

    # join components in the right order (base + accents)
    components = baseGlyphs + accentGlyphs

    # make glyph construction
    construction = '%s = ' % glyph.name
    for i, gName in enumerate(components):
        construction += gName
        if i < len(components) - 1:
            construction += ' + '

    # done
    return construction
