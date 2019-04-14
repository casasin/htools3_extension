# coding: utf-8

from __future__ import print_function

import os
from mojo.roboFont import OpenFont
from vanilla import *
from vanilla.dialogs import getFile
from hTools3.dialogs import hDialog

class ImportGlyphsIntoLayerDialog(hDialog):

    '''
    A dialog to import glyphs from a font file into a layer of the selected glyphs.

    .. code-block:: python

        from hTools3.dialogs.glyphs.layersImport import ImportGlyphsIntoLayerDialog
        ImportGlyphsIntoLayerDialog()

    '''

    title = 'import'
    key = '%s.glyphs.layersImport' % hDialog.key
    sourceFont = None

    def __init__(self):
        self.height  = self.buttonHeight * 2
        self.height += self.textHeight * 5
        self.height += self.padding * 8
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        self.w.getFile = SquareButton(
                (x, y, -p, self.buttonHeight),
                "get ufo...",
                callback=self.getFontCallback,
                sizeStyle=self.sizeStyle)

        y += self.buttonHeight + p
        self.w.sourceLayerLabel = TextBox(
                (x, y, -p, self.textHeight),
                "source layer",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.sourceLayers = PopUpButton(
                (x, y, -p, self.textHeight),
                [],
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.targetLayerLabel = TextBox(
                (x, y, -p, self.textHeight),
                "target layer",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.targetLayer = RadioGroup(
                (x, y, -p, self.textHeight * 2),
                ["font name", "custom"],
                isVertical=True,
                sizeStyle=self.sizeStyle)
        self.w.targetLayer.set(0)

        y += self.textHeight * 2 + p
        self.w.targetLayerName = EditText(
                (x, y, -p, self.textHeight),
                "",
                placeholder='layer name',
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.applyButton = SquareButton(
                (x, y, -p, self.buttonHeight),
                "import",
                callback=self.applyCallback,
                sizeStyle=self.sizeStyle)

        self.w.open()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def sourceLayer(self):
        i = self.w.sourceLayers.get()
        return self.w.sourceLayers.getItems()[i]

    @property
    def targetLayer(self):
        if self.w.targetLayer.get() == 0:
            return '%s %s %s' % (self.sourceFont.info.familyName, self.sourceFont.info.styleName, self.sourceLayer)
        else:
            layerName = self.w.targetLayerName.get()
            if len(layerName):
                return layerName
            else:
                return 'untitled'

    # ---------
    # callbacks
    # ---------

    def getFontCallback(self, sender):
        ufoPath = getFile()[0]
        self.sourceFont = OpenFont(ufoPath, showInterface=False)
        self.w.sourceLayers.setItems(self.sourceFont.layerOrder)

    def applyCallback(self, sender):
        self.apply()

    # -------
    # methods
    # -------

    def apply(self):

        # -----------------
        # assert conditions
        # -----------------

        font = self.getCurrentFont()
        if not font:
            return

        if not self.sourceFont:
            print('no source font selected.\n')
            return

        glyphNames = self.getGlyphNames()
        if not glyphNames:
            return

        # ----------
        # print info
        # ----------

        if self.verbose:
            print('importing glyphs into layer...\n')
            print('\tsource font: %s %s' % (self.sourceFont.info.familyName, self.sourceFont.info.styleName))
            print('\tsource layer: %s' % self.sourceLayer)
            print('\ttarget layer: %s' % self.targetLayer)
            print()
            print('\t', end='')
            print(' '.join(glyphNames), end='\n')

        # -----------
        # copy glyphs
        # -----------

        for glyphName in glyphNames:

            if not glyphName in self.sourceFont:
                continue

            sourceGlyph = self.sourceFont[glyphName].getLayer(self.sourceLayer)
            targetGlyph = font[glyphName].getLayer(self.targetLayer)

            pen = targetGlyph.getPointPen()
            sourceGlyph.drawPoints(pen)
            targetGlyph.width = sourceGlyph.width

            targetGlyph.changed()

        # done
        font.changed()
        if self.verbose:
            print('\n...done.\n')

# -------
# testing
# -------

if __name__ == '__main__':

    ImportGlyphsIntoLayerDialog()
