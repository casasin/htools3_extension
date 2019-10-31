# coding: utf-8

from __future__ import print_function

from importlib import reload
import hTools3.dialogs.glyphs.base
reload(hTools3.dialogs.glyphs.base)

from vanilla import CheckBox, SquareButton
from mojo import drawingTools as ctx
from mojo.UI import getDefault
from hTools3.dialogs.glyphs.base import GlyphsDialogBase
from hTools3.dialogs.misc.spinner import Spinner

def moveGlyphFactory():
    pass

class MoveGlyphsDialog(GlyphsDialogBase):

    '''
    A dialog to move selected glyphs in the current font.

    .. code-block:: python

        from hTools3.dialogs.glyphs.move import MoveGlyphsDialog
        MoveGlyphsDialog()

    '''

    title = "move"
    key = '%s.move' % GlyphsDialogBase.key
    settings = {
        'moveValueX' : 70,
        'moveValueY' : 0,
    }

    def __init__(self):
        self.height  = self.spinnerHeight * 2
        self.height += self.buttonHeight
        self.height += self.textHeight
        self.height += self.padding * 5 + 2
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        self.w.spinnerX = Spinner(
                (x, y),
                default=self.settings['moveValueX'],
                integer=True,
                callback=self.updatePreviewCallback,
                label='delta x')

        y += self.w.spinnerX.height + p + 2
        self.w.spinnerY = Spinner(
                (x, y),
                default=self.settings['moveValueY'],
                integer=True,
                callback=self.updatePreviewCallback,
                label='delta y')

        y += self.w.spinnerY.height + p + 2
        self.w.applyButton = SquareButton(
                (x, y, -p, self.buttonHeight),
                'apply',
                sizeStyle=self.sizeStyle,
                callback=self.applyCallback)

        y += self.buttonHeight + p
        self.w.preview = CheckBox(
                (x, y, -p, self.textHeight),
                "preview",
                value=True,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        self.initGlyphsWindowBehaviour()

        self.w.open()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def moveValues(self):
        dx = self.w.spinnerX.value
        dy = self.w.spinnerY.value
        return dx, dy

    #-----------
    # observers
    #-----------

    def backgroundPreview(self, notification):

        g = notification['glyph']
        s = notification['scale']

        # assert conditions

        if not self.w.preview.get():
            return

        if not g:
            return

        if not g.bounds:
            return

        # get parameters
        dx = self.w.spinnerX.value
        dy = self.w.spinnerY.value

        # make preview
        previewGlyph = self.makeGlyph(g, (dx, dy), preview=True)

        # draw preview
        if notification['notificationName'] == 'drawBackground':
            self.drawPreview(previewGlyph, s)
        else:
            self.drawPreview(previewGlyph, s, plain=True)

    #---------
    # methods
    #---------

    def drawPreview(self, glyph, previewScale, plain=False):

        ctx.save()

        if not plain:
            ctx.fill(*self.previewFillColor)
            ctx.stroke(*self.previewStrokeColor)
            ctx.strokeWidth(self.previewStrokeWidth * previewScale)
        else:
            w = getDefault("glyphViewDefaultWidth")
            h = getDefault("glyphViewDefaultHeight")
            ctx.stroke(None)
            ctx.fill(1)
            ctx.rect(-w * previewScale, -h * previewScale, w * previewScale * 2, h * previewScale * 2)
            ctx.fill(0)

        ctx.drawGlyph(glyph)

        ctx.restore()

    def makeGlyph(self, glyph, preview=False):
        if preview:
            glyph = glyph.copy()

        # apply move
        glyph.moveBy(self.moveValues)

        # done
        return glyph

    def apply(self):

        # -----------------
        # assert conditions
        # -----------------

        font = self.getCurrentFont()
        if not font:
            return

        glyphNames = self.getGlyphNames()
        if not glyphNames:
            return

        layerNames = self.getLayerNames()
        if not layerNames:
            layerNames = [font.defaultLayer.name]

        # ----------
        # print info
        # ----------

        if self.verbose:
            print('moving glyphs:\n')
            print(f'\tdistance: {self.moveValues[0]}, {self.moveValues[1]}')
            print(f'\tlayers: {", ".join(layerNames)}')
            print(f'\tglyphs: {", ".join(glyphNames)}')

        # ----------------
        # transform glyphs
        # ----------------

        for glyphName in glyphNames:
            for layerName in layerNames:
                g = font[glyphName].getLayer(layerName)
                g.prepareUndo('move glyphs')
                self.makeGlyph(g)
                g.changed()
                g.performUndo()

        # done
        font.changed()
        if self.verbose:
            print('\n...done.\n')

#---------
# testing
#---------

if __name__ == "__main__":

    MoveGlyphsDialog()
