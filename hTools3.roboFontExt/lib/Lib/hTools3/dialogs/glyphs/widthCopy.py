# coding: utf-8

from __future__ import print_function

from vanilla import TextBox, PopUpButton, SquareButton, List
from mojo.roboFont import AllFonts
from mojo.events import addObserver, removeObserver
from defconAppKit.windows.baseWindow import BaseWindowController
from hTools3.dialogs import hDialog

class CopyWidthDialog(hDialog, BaseWindowController):

    '''
    A dialog to copy the width from selected glyphs in one font to the same glyphs in another font or layer.

    .. code-block:: python

        from hTools3.dialogs.glyphs.widthCopy import CopyWidthDialog
        CopyWidthDialog()

    '''

    title = 'widths'
    key = '%s.glyphs.widthCopy' % hDialog.key

    allFonts = {}

    def __init__(self):
        self.height  = self.buttonHeight
        self.height += self.textHeight * 5
        self.height += self.padding * 4.5
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        y -= 2
        self.w.sourceLabel = TextBox(
                (x, y, -p, self.textHeight),
                "source",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.sourceLayer = PopUpButton(
                (x, y, -p, self.textHeight),
                [],
                callback=self.updateSourceLayerCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.targetLabel = TextBox(
                (x, y, -p, self.textHeight),
                "target",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.targetFont = PopUpButton(
                (x, y, -p, self.textHeight),
                [],
                callback=self.updateTargetFontCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p * 0.5
        self.w.targetLayer = PopUpButton(
                (x, y, -p, self.textHeight),
                [],
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.apply = SquareButton(
                (x, y, -p, self.buttonHeight),
                "copy",
                callback=self.applyCallback,
                sizeStyle=self.sizeStyle)

        self.updateSourceLayer()
        self.updateTargetFonts()
        self.updateTargetLayers()

        self.setUpBaseWindowBehavior()

        addObserver(self, 'updateListsObserver', 'currentGlyphChanged')
        addObserver(self, 'updateListsObserver', 'newFontDidOpen')
        addObserver(self, 'updateListsObserver', 'fontDidOpen')
        addObserver(self, 'updateListsObserver', 'fontDidClose')

        self.w.open()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def sourceFont(self):
        return self.getCurrentFont()

    @property
    def sourceLayer(self):
        i = self.w.sourceLayer.get()
        return self.w.sourceLayer.getItems()[i]

    @property
    def targetFont(self):
        i = self.w.targetFont.get()
        fontName = self.w.targetFont.getItems()[i]
        return self.allFonts.get(fontName)

    @property
    def targetLayer(self):
        i = self.w.targetLayer.get()
        return self.w.targetLayer.getItems()[i]

    # ---------
    # observers
    # ---------

    def updateListsObserver(self, sender):
        self.updateSourceLayer()
        self.updateTargetFonts()
        self.updateTargetLayers()

    # ---------
    # callbacks
    # ---------

    def windowCloseCallback(self, sender):
        super().windowCloseCallback(sender)
        removeObserver(self, 'currentGlyphChanged')
        removeObserver(self, 'newFontDidOpen')
        removeObserver(self, 'fontDidOpen')
        removeObserver(self, 'fontDidClose')

    def updateSourceLayerCallback(self, sender):
        self.updateTargetLayers()

    def updateTargetFontCallback(self, sender):
        self.updateTargetLayers()

    def applyCallback(self, sender):
        self.apply()

    # -------
    # methods
    # -------

    def updateSourceLayer(self):

        if not self.sourceFont:
            self.w.sourceLayer.setItems([])
            return

        self.w.sourceLayer.setItems(self.sourceFont.layerOrder)

    def updateTargetFonts(self):

        if not self.sourceFont:
            self.w.targetFont.setItems([])
            return

        self.allFonts = {'%s %s' % (f.info.familyName, f.info.styleName) : f for f in AllFonts()}
        self.w.targetFont.setItems(self.allFonts.keys())

    def updateTargetLayers(self):

        sourceFont = self.getCurrentFont()
        targetFont = self.targetFont

        if not targetFont:
            self.w.targetLayer.setItems([])
            return

        targetLayers = targetFont.layerOrder

        if sourceFont == targetFont:
            targetLayers.remove(self.sourceLayer)

        self.w.targetLayer.setItems(targetLayers)

    def apply(self):

        # -----------------
        # assert conditions
        # -----------------

        sourceFont = self.sourceFont
        if not sourceFont:
            return

        glyphNames = self.getGlyphNames()
        if not glyphNames:
            return

        targetFont = self.targetFont

        # ----------
        # print info
        # ----------

        if self.verbose:
            sourceFontName = '%s %s' % (sourceFont.info.familyName, sourceFont.info.styleName)
            targetFontName = '%s %s' % (targetFont.info.familyName, targetFont.info.styleName)
            print('copying glyph widths:\n')
            print('\tsource: %s > %s' % (sourceFontName, self.sourceLayer))
            print('\ttarget: %s > %s' % (targetFontName, self.targetLayer))
            print()
            print('\t', end='')
            print(' '.join(glyphNames), end='\n')

        # -----------
        # copy widths
        # -----------

        for glyphName in glyphNames:
            sourceGlyph = sourceFont[glyphName].getLayer(self.sourceLayer)
            targetGlyph = targetFont[glyphName].getLayer(self.targetLayer)
            targetGlyph.prepareUndo('copy width')
            targetGlyph.width = sourceGlyph.width
            targetGlyph.changed()
            targetGlyph.performUndo()

        # done
        targetFont.changed()
        if self.verbose:
            print('\n...done.\n')

# -------
# testing
# -------

if __name__ == "__main__":

    CopyWidthDialog()
