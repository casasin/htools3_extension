# coding: utf-8

'''
Tools to work with ``mark`` feature code.

'''

class markToBaseFeaBuilder(object):

    '''
    An object to create mark feature code from a list of base & mark glyphs with named anchors.

    .. code-block:: python

        from hTools3.modules.markFeature import markToBaseFeaBuilder

        f = CurrentFont()

        markToBaseDict = {
            'x'     : [('tilde', 'top'), ('grave', 'top'), ('dotaccent', 'bottom')],
            'X'     : [('tilde', 'top')],
            'one'   : [('tilde', 'top'), ('dotaccent', 'bottom')],
            'two'   : [('grave', 'top')],
            'three' : [('tilde', 'top')],
        }

        M = markToBaseFeaBuilder(f, markToBaseDict)
        M.verbose = True
        M.buildDicts()
        M.write()

        print(f.features.text)

    '''

    verbose = True

    def __init__(self, font, markToBaseDict):
        self.font = font
        self.markToBaseDict = markToBaseDict
        self.marksDict = {}
        self.basesDict = {}

    @property
    def allBases(self):
        return self.basesDict.keys()

    @property
    def allMarks(self):
        return self.marksDict.keys()

    @property
    def allMarkClasses(self):
        return [self.makeMarkClassName(m) for m in self.allMarks]

    @property
    def fontName(self):
        return '%s %s' % (self.font.info.familyName, self.font.info.styleName)

    def makeMarkClassName(self, markName):
        return '@%s_marks' % markName

    def writeMarkClasses(self):
        txt = ''
        for markName in self.marksDict.keys():
            markClassName = self.makeMarkClassName(markName)
            for markGlyph, markAnchorPos in self.marksDict[markName]:
                txt += 'markClass '
                txt += '[%s] ' % markGlyph
                txt += '<anchor %s %s> ' % markAnchorPos
                txt += '%s;\n' % markClassName
        return txt

    def writeMarkFeature(self):
        txt = 'feature mark {\n\n'
        for markName in self.allMarks:
            lookupName = 'base_%s' % markName
            txt += '\tlookup %s {\n' % lookupName
            for baseGlyph in self.basesDict.keys():
                if markName in self.basesDict[baseGlyph]:
                    markClassName = self.makeMarkClassName(markName)
                    baseAnchorPos = self.basesDict[baseGlyph][markName][0]
                    txt += '\t\tpos base [%s] ' % baseGlyph
                    txt += '<anchor %s %s> ' % baseAnchorPos
                    txt += 'mark %s;\n' % markClassName
            txt += '\t} %s;\n\n' % lookupName
        txt += '} mark;\n'
        return txt

    def writeTableGDEF(self):
        txt  = '@allBases = [%s];\n' % ' '.join(self.allBases)
        txt += '@allMarks = [%s];\n' % ' '.join(self.allMarkClasses)
        txt += '\n'
        txt += 'table GDEF {\n'
        txt += '\tGlyphClassDef @allBases,,@allMarks,;\n'
        txt += '} GDEF;\n'
        txt += '\n'
        return txt

    def buildDicts(self):

        self.marksDict = {}
        self.basesDict = {}

        for baseGlyph, markGlyphs in self.markToBaseDict.items():

            if not baseGlyph in self.font:
                if self.verbose:
                    print("[PROBLEM] base glyph '%s' not in font '%s'." % (baseGlyph, self.fontName))
                continue

            for markGlyph, anchorName in markGlyphs:

                if not markGlyph in self.font:
                    if self.verbose:
                        print("[PROBLEM] mark glyph '%s' not in font '%s'." % (markGlyph, self.fontName))
                    continue

                # get mark anchor
                markAnchor = [a for a in self.font[markGlyph].anchors if a.name == '_%s' % anchorName]
                if not len(markAnchor):
                    if self.verbose:
                        print("[PROBLEM] mark glyph '%s' has no anchor '_%s'." % (markGlyph, anchorName))
                    continue

                markAnchor = markAnchor[0]
                markAnchorPos = int(markAnchor.position[0]), int(markAnchor.position[1])

                # get base anchor
                baseAnchor = [a for a in self.font[baseGlyph].anchors if a.name == '%s' % anchorName]
                if not len(baseAnchor):
                    if self.verbose:
                        print("[PROBLEM] base glyph '%s' has no anchor '%s'." % (baseGlyph, anchorName))
                    continue

                baseAnchor = baseAnchor[0]
                baseAnchorPos = int(baseAnchor.position[0]), int(baseAnchor.position[1])

                # save mark data
                if anchorName not in self.marksDict:
                    self.marksDict[anchorName] = []

                markItem = markGlyph, markAnchorPos

                if not markItem in self.marksDict[anchorName]:
                    if self.verbose:
                        print("[OK] anchor '%s' %s found in mark glyph '%s'..." % (anchorName, markAnchorPos, markGlyph))
                    self.marksDict[anchorName].append(markItem)

                # save base data
                if baseGlyph not in self.basesDict:
                    self.basesDict[baseGlyph] = {}

                if anchorName not in self.basesDict[baseGlyph]:
                    self.basesDict[baseGlyph][anchorName] = [baseAnchorPos, []]

                if markGlyph not in self.basesDict[baseGlyph][anchorName][1]:
                    if self.verbose:
                        print("[OK] anchor '%s' %s found in mark glyph '%s'..." % (anchorName, baseAnchorPos, baseGlyph))
                    self.basesDict[baseGlyph][anchorName][1].append(markGlyph)

    def compile(self):
        self.buildDicts()
        txt = ''
        txt += self.writeMarkClasses()
        txt += '\n'
        txt += self.writeMarkFeature()
        txt += '\n'
        txt += self.writeTableGDEF()
        return txt

    def write(self, langsystem=True):
        txt = ''
        if langsystem:
            txt += 'languagesystem DFLT dflt;\n'
            txt += 'languagesystem latn dflt;\n'
            txt += '\n'
        txt += self.compile()
        self.font.features.text = txt
