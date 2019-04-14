# coding: utf-8

from __future__ import print_function

from importlib import reload
import hTools3.dialogs.glyphs.base
reload(hTools3.dialogs.glyphs.base)

from vanilla import CheckBox, SquareButton, RadioGroup
from mojo import drawingTools as ctx
from mojo.UI import getDefault
from hTools3.dialogs.glyphs.base import GlyphsDialogBase
from hTools3.dialogs.misc.origin import OriginPoint
from hTools3.dialogs.misc.spinner import Spinner
from hTools3.modules.glyphutils import getOriginPosition

def scaleGlyphFactory():
    pass

class ScaleGlyphsDialog(GlyphsDialogBase):

    '''
    A dialog to scale selected glyphs in the current font.

    .. code-block:: python

        from hTools3.dialogs.glyphs.scale import ScaleGlyphsDialog
        ScaleGlyphsDialog()

    '''

    title = "scale"
    key = '%s.scale' % GlyphsDialogBase.key
    settings = {
        'xMetrics'           : False,
        'yMetrics'           : False,
        'scaleValue'         : 1.10,
        'spinnerScaleFactor' : 0.01,
    }

    def __init__(self):
        self.height  = self.width
        self.height += self.spinnerHeight
        self.height += self.buttonHeight
        self.height += self.textHeight * 4
        self.height += self.padding * 5 - 2
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        self.w.origin = OriginPoint(
                (x, y, self.width, self.width),
                callback=self.updatePreviewCallback)
        self.w.origin.setPosition(None)

        y += self.w.origin.height - p
        self.w.spinnerScale = Spinner(
                (x, y),
                default=self.settings['scaleValue'],
                scale=self.settings['spinnerScaleFactor'],
                integer=False,
                callback=self.updatePreviewCallback,
                label='factor')

        x = p * 0.6
        y += self.w.spinnerScale.height + p + 2
        self.w.scaleMode = RadioGroup(
                (x, y, -p * 0.5, self.textHeight),
                ["xy", "xx", "yy"],
                isVertical=False,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)
        self.w.scaleMode.set(0)

        x = p
        y += self.textHeight + p - 2
        self.w.metricsX = CheckBox(
                (x, y, -p, self.textHeight),
                "side bearings",
                value=self.settings['xMetrics'],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.metricsY = CheckBox(
                (x, y, -p, self.textHeight),
                "vertical metrics",
                value=self.settings['yMetrics'],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
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
    def scaleFactors(self):
        # get settings
        value = self.w.spinnerScale.value
        scaleMode = self.w.scaleMode.get()

        # horizontal
        if scaleMode == 1:
            valueX, valueY = value, 1

        # vertical
        elif scaleMode == 2:
            valueX, valueY = 1, value

        # proportional
        else:
            valueX = valueY = value

        return valueX, valueY

    @property
    def posName(self):
        return self.w.origin.selected

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

        if not g.bounds:
            return

        # make preview
        previewGlyph = self.makeGlyph(g, preview=True)

        # draw preview
        if notification['notificationName'] == 'drawBackground':
            self.drawPreview(g, previewGlyph, s)
        else:
            self.drawPreview(g, previewGlyph, s, plain=True)

    # -------
    # methods
    # -------

    def getOriginPos(self, glyph):
        if self.posName:
            return getOriginPosition(glyph, self.posName)
        else:
            return 0, 0

    def drawPreview(self, srcGlyph, previewGlyph, previewScale, plain=False):

        scaleX, scaleY = self.scaleFactors

        ctx.save()

        # draw glyph
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

        ctx.drawGlyph(previewGlyph)

        if not plain:
            # draw origin
            r = self.previewOriginRadius * previewScale
            x, y = self.getOriginPos(srcGlyph)
            ctx.fill(None)
            ctx.line((x - r, y), (x + r, y))
            ctx.line((x, y - r), (x, y + r))
            ctx.oval(x - r, y - r, r * 2, r * 2)

            ctx.lineDash(self.previewStrokeWidth * previewScale, self.previewStrokeWidth * previewScale)

            # draw advance width
            if self.w.metricsX.get():
                if previewGlyph.bounds:
                    leftMargin  = srcGlyph.leftMargin
                    rightMargin = srcGlyph.rightMargin
                    leftMargin  *= scaleX
                    rightMargin *= scaleX
                    L, B, R, T = previewGlyph.bounds
                    x1 = L - leftMargin
                    x2 = R + rightMargin
                    y1 = -10000
                    y2 = 10000
                    ctx.line((x1, y1), (x1, y2))
                    ctx.line((x2, y1), (x2, y2))
                else:
                    # TODO: x-scale should also work with empty glyphs
                    pass

            # draw vertical metrics
            if self.w.metricsY.get():
                x1 = -10000
                x2 = 10000
                yLines = [
                    srcGlyph.font.info.xHeight,
                    srcGlyph.font.info.descender,
                    srcGlyph.font.info.ascender,
                    srcGlyph.font.info.capHeight,
                ]
                yLines = set([y * scaleY for y in yLines])
                for y in yLines:
                    ctx.line((x1, y), (x2, y))

        ctx.restore()

    def makeGlyph(self, glyph, preview=False):
        if preview:
            glyph = glyph.copy()
        else:
            # cache original margins
            left  = glyph.leftMargin
            right = glyph.rightMargin

        # apply scale
        originPos = self.getOriginPos(glyph)
        glyph.scaleBy(self.scaleFactors, origin=originPos)

        # scale horizontal metrics
        if not preview:
            glyph.leftMargin  = left  * self.scaleFactors[0]
            glyph.rightMargin = right * self.scaleFactors[0]

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

        # ----------
        # print info
        # ----------

        if self.verbose:
            print('scaling glyphs:\n')
            print('\tscale: %s, %s' % self.scaleFactors)
            print('\torigin: %s' % self.posName)
            print()
            print('\t', end='')
            print(', '.join(glyphNames), end='\n')

        # ----------------
        # transform glyphs
        # ----------------

        for glyphName in glyphNames:
            g = font[glyphName]
            # scale glyph
            g.prepareUndo('scale')
            self.makeGlyph(g)
            g.changed()
            g.performUndo()

        # scale vertical metrics
        if self.w.metricsY.get():
            font.info.xHeight   *= self.scaleFactors[1]
            font.info.capHeight *= self.scaleFactors[1]
            font.info.ascender  *= self.scaleFactors[1]
            font.info.descender *= self.scaleFactors[1]

        # done
        font.changed()
        if self.verbose:
            print('\n...done.\n')

# -------
# testing
# -------

if __name__ == "__main__":

    ScaleGlyphsDialog()
