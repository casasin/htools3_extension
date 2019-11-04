# coding: utf-8

from __future__ import print_function

from importlib import reload
import hTools3.dialogs.glyphs.base
reload(hTools3.dialogs.glyphs.base)
import hTools3.modules.glyphutils
reload(hTools3.modules.glyphutils)

from vanilla import RadioGroup, CheckBox, SquareButton
from mojo import drawingTools as ctx
from hTools3.dialogs.glyphs.base import GlyphsDialogBase
from hTools3.dialogs.misc.spinner import Spinner
from hTools3.modules.glyphutils import setGlyphWidth

class SetWidthDialog(GlyphsDialogBase):

    '''
    A dialog to set the width of selected glyphs in the current font.

    .. code-block:: python

        from hTools3.dialogs.glyphs.widthSet import SetWidthDialog
        SetWidthDialog()

    '''

    title = 'width'
    key = '%s.width' % GlyphsDialogBase.key
    settings = {
        'widthValue' : 400,
        'mode'       : 0,
    }

    modes = [
        'set equal to',
        'increase by',
        'decrease by'
    ]

    positionOptions = [
        'do not move',
        'center glyph',
        'split margins',
        'relative split'
    ]

    def __init__(self):
        self.height  = self.spinnerHeight
        self.height += self.buttonHeight
        self.height += self.textHeight * 6
        self.height += self.padding * 6
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        self.w.widthMode = RadioGroup(
                (x, y, -p, self.textHeight),
                ['=', '+', '-'],
                sizeStyle=self.sizeStyle,
                callback=self.updatePreviewCallback,
                isVertical=False)
        self.w.widthMode.set(0)

        y += self.textHeight + self.padding
        self.w.widthValue = Spinner(
                (x, y),
                default=self.settings['widthValue'],
                integer=True,
                callback=self.updatePreviewCallback,
                label='width')

        y += self.w.widthValue.height + p
        self.w.positionMode = RadioGroup(
                (x, y, -p, self.textHeight*4),
                self.positionOptions,
                sizeStyle=self.sizeStyle,
                callback=self.updatePreviewCallback,
                isVertical=True)
        self.w.positionMode.set(0)

        y += self.textHeight * len(self.positionOptions) + p
        self.w.buttonApply = SquareButton(
                (x, y, -p, self.buttonHeight),
                "apply",
                callback=self.applyCallback,
                sizeStyle=self.sizeStyle)

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
    def widthValue(self):
        return self.w.widthValue.value

    @property
    def widthMode(self):
        return self.modes[self.w.widthMode.get()]

    @property
    def positionMode(self):
        return self.positionOptions[self.w.positionMode.get()]

    # ---------
    # observers
    # ---------

    def backgroundPreview(self, notification):

        g = notification['glyph']
        s = notification['scale']

        # assert conditions

        if not self.w.preview.get():
            return

        if not g:
            return

        # make preview

        previewGlyph = self.makeGlyph(g, preview=True)

        # draw preview

        self.drawPreview(g, previewGlyph, s)

    # -------
    # methods
    # -------

    def drawPreview(self, glyph, previewGlyph, previewScale):
        dx = previewGlyph.leftMargin - glyph.leftMargin
        x1, x2 = 0, previewGlyph.width
        y1, y2 = -10000, 10000
        ctx.save()
        ctx.fill(*self.previewFillColor)
        ctx.stroke(*self.previewStrokeColor)
        ctx.strokeWidth(self.previewStrokeWidth * previewScale)
        ctx.translate(-dx, 0)
        ctx.drawGlyph(previewGlyph)
        ctx.lineDash(self.previewStrokeWidth * previewScale, self.previewStrokeWidth * previewScale)
        ctx.line((x1, y1), (x1, y2))
        ctx.line((x2, y1), (x2, y2))
        ctx.restore()

    def makeGlyph(self, glyph, preview=False):
        if preview:
            glyph = glyph.copy()

        if self.widthMode == 'increase by':
            widthNew = glyph.width + self.widthValue
        elif self.widthMode == 'decrease by':
            widthNew = glyph.width - self.widthValue
        else:
            widthNew = self.widthValue

        setGlyphWidth(glyph, widthNew, self.positionMode)

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
            print('setting glyph widths:\n')
            print(f'\tvalue: {self.widthValue}')
            print(f'\tmode: {self.widthMode}')
            print(f'\tposition: {self.positionMode}')
            print(f'\tlayers: {", ".join(layerNames)}')
            print(f'\tglyphs: {", ".join(glyphNames)}')

        # ----------------
        # transform glyphs
        # ----------------

        for glyphName in glyphNames:
            for layerName in layerNames:
                g = font[glyphName].getLayer(layerName)
                g.prepareUndo('set width')
                self.makeGlyph(g)
                g.changed()
                g.performUndo()

        # done
        font.changed()
        if self.verbose:
            print('\n...done.\n')

# -------
# testing
# -------

if __name__ == "__main__":

    SetWidthDialog()