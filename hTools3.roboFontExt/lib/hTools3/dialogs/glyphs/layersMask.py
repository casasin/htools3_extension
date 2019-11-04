# coding: utf-8

from vanilla import PopUpButton, SquareButton, CheckBox, TextBox
from mojo.roboFont import AllFonts
from mojo.events import addObserver, removeObserver
from defconAppKit.windows.baseWindow import BaseWindowController
from hTools3.dialogs import hDialog

# TODO: add observers for layerset changes
# update UI when adding/deleting/renaming layers

class MaskDialog(hDialog, BaseWindowController):

    '''
    A dialog to transfer glyphs between main layer and mask layer.

    .. code-block:: python

        from hTools3.dialogs.glyphs.layersMask import MaskDialog
        MaskDialog()

    '''

    title = 'mask'
    key = '{}.glyphs.layers.mask'.format(hDialog.key)

    def __init__(self):
        self.height  = self.buttonHeight * 3
        self.height += self.textHeight * 5
        self.height += self.padding * 6.5
        self.w = self.window((self.width, self.height), self.title)

        x = p = self.padding
        y = p - 5
        self.w.sourceLayerLabel = TextBox(
                (x, y, -p, self.textHeight),
                'main layer',
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.sourceLayer = PopUpButton(
                (x, y, -p, self.textHeight),
                [],
                callback=self.updateSourceLayerCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p # - 5
        self.w.maskLayerLabel = TextBox(
                (x, y, -p, self.textHeight),
                'mask layer',
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.maskLayers = PopUpButton(
                (x, y, -p, self.textHeight),
                [],
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p + 5
        self.w.copyButton = SquareButton(
                (x, y, -p, self.buttonHeight),
                "copy",
                sizeStyle=self.sizeStyle,
                callback=self.copyCallback)

        y += self.buttonHeight + p
        self.w.switchButton = SquareButton(
                (x, y, -p, self.buttonHeight),
                "flip",
                sizeStyle=self.sizeStyle,
                callback=self.flipLayersCallback)

        y += self.buttonHeight + p
        self.w.clearButton = SquareButton(
                (x, y, -p, self.buttonHeight),
                "clear",
                sizeStyle=self.sizeStyle,
                callback=self.clearMaskCallback)

        y += self.buttonHeight + p
        self.w.lockLayerWidths = CheckBox(
                (x, y, -p, self.textHeight),
                'lock widths',
                value=False,
                sizeStyle=self.sizeStyle)

        self.updateSourceLayer()
        self.updateMaskLayersList()

        self.setUpBaseWindowBehavior()

        addObserver(self, 'updateLayersObserver', 'currentGlyphChanged')
        addObserver(self, 'updateLayersObserver', 'newFontDidOpen')
        addObserver(self, 'updateLayersObserver', 'fontDidOpen')
        addObserver(self, 'updateLayersObserver', 'fontDidClose')

        self.w.open()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def sourceLayer(self):
        i = self.w.sourceLayer.get()
        return self.w.sourceLayer.getItems()[i]

    @property
    def maskLayer(self):
        i = self.w.maskLayers.get()
        return self.w.maskLayers.getItems()[i]

    @property
    def lockLayerWidths(self):
        return self.w.lockLayerWidths.get()

    # ---------
    # observers
    # ---------

    def updateLayersObserver(self, sender):
        self.updateSourceLayer()
        self.updateMaskLayersList()

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
        font = self.getCurrentFont()
        if not font:
            return
        self.updateMaskLayersList()

    def flipLayersCallback(self, sender):
        '''
        Flip contents between source layer and mask layer.

        '''
        font = self.getCurrentFont()
        if not font:
            return

        glyphNames = self.getGlyphNames()
        if not glyphNames:
            return

        for glyphName in glyphNames:
            g = font[glyphName]
            g.flipLayers(self.sourceLayer, self.maskLayer)

            if self.lockLayerWidths:
                sourceGlyph = font[glyphName].getLayer(self.sourceLayer)
                maskGlyph   = font[glyphName].getLayer(self.maskLayer)
                maskGlyph.width = sourceGlyph.width

    def clearMaskCallback(self, sender):
        '''
        Clear mask layer in selected glyphs.

        '''
        font = self.getCurrentFont()
        if not font:
            return

        glyphNames = self.getGlyphNames()
        if not glyphNames:
            return

        for glyphName in glyphNames:
            g = font[glyphName].getLayer(self.maskLayer)
            g.prepareUndo('clear mask layer')
            g.clear()
            g.performUndo()

    def copyCallback(self, sender):
        '''
        Copy foreground layer to mask layer.

        '''
        font = self.getCurrentFont()
        if not font:
            return

        glyphNames = self.getGlyphNames()
        if not glyphNames:
            return

        for glyphName in glyphNames:
            g = font[glyphName].getLayer(self.sourceLayer)
            g.copyToLayer(self.maskLayer, clear=False)

            if self.lockLayerWidths:
                sourceGlyph = font[glyphName].getLayer(self.sourceLayer)
                maskGlyph   = font[glyphName].getLayer(self.maskLayer)
                maskGlyph.width = sourceGlyph.width

    # -------
    # methods
    # -------

    def updateSourceLayer(self):
        '''
        Update source layer pop-up list based on the current font.

        '''
        font = self.getCurrentFont()
        if not font:
            self.w.sourceLayer.setItems([])
        else:
            self.w.sourceLayer.setItems(font.layerOrder)

    def updateMaskLayersList(self):
        '''
        Update mask layer pop-up list based on the current font.

        '''
        font = self.getCurrentFont()
        if not font:
            self.w.maskLayers.setItems([])
        else:
            maskLayers = list(font.layerOrder)
            maskLayers.remove(self.sourceLayer)
            self.w.maskLayers.setItems(maskLayers)

# -------
# testing
# -------

if __name__ == "__main__":

    MaskDialog()
