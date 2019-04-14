# coding: utf-8

from __future__ import print_function

from vanilla import TextBox, RadioGroup, SquareButton, CheckBox
from mojo import drawingTools as ctx
from hTools3.dialogs.glyphs.base import GlyphsDialogBase
from hTools3.dialogs.misc.spinner import Spinner
from hTools3.modules.glyphutils import deselectPoints, selectPointsLine, shiftSelectedPoints

class ShiftPointsDialog(GlyphsDialogBase):

    title = 'shift points'
    key = '%s.pointsShift' % GlyphsDialogBase.key
    settings = {
        'axis'      : 1,
        'side'      : 1,
        'pos'       : 250,
        'delta'     : 100,
        'direction' : 1,
    }

    glyphNames = []

    def __init__(self):
        self.height  = self.spinnerHeight * 2
        self.height += self.textHeight * 4
        self.height += self.buttonHeight
        self.height += self.padding * 7.3
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        col = (self.width - p * 2) * 0.5
        self.w.spinnerPos = Spinner(
                (x, y),
                default=self.settings['pos'],
                integer=True,
                callback=self.updatePreviewCallback,
                label='pos')

        y += self.w.spinnerPos.height + p
        self.w.axisLabel = TextBox(
                (x, y, col, self.textHeight),
                "axis",
                sizeStyle=self.sizeStyle)

        x = col
        self.w.axis = RadioGroup(
                (x, y, -p, self.textHeight),
                ["x", "y"],
                sizeStyle=self.sizeStyle,
                callback=self.updatePreviewCallback,
                isVertical=False)
        self.w.axis.set(self.settings['axis'])

        x = p
        y += self.textHeight + p * 0.5
        self.w.sideLabel = TextBox(
                (x, y, col, self.textHeight),
                "side",
                sizeStyle=self.sizeStyle)
        x = col
        self.w.side = RadioGroup(
                (x, y, -p, self.textHeight),
                ["-", "+"],
                sizeStyle=self.sizeStyle,
                callback=self.updatePreviewCallback,
                isVertical=False)
        self.w.side.set(self.settings['direction'])

        x = p
        y += self.textHeight + p
        self.w.spinnerDelta = Spinner(
                (x, y),
                default=self.settings['delta'],
                integer=True,
                callback=self.updatePreviewCallback,
                label='delta')

        y += self.w.spinnerDelta.height + p
        self.w.shiftDirectionLabel = TextBox(
                (x, y, col, self.textHeight),
                "shift",
                sizeStyle=self.sizeStyle)
        x = col
        self.w.shiftDirection = RadioGroup(
                (x, y, -p, self.textHeight),
                ["-", "+"],
                sizeStyle=self.sizeStyle,
                callback=self.updatePreviewCallback,
                isVertical=False)
        self.w.shiftDirection.set(self.settings['side'])

        x = p
        y += self.textHeight + p
        self.w.buttonApply = SquareButton(
                (x, y, -p, self.buttonHeight),
                "apply",
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
    def position(self):
        return self.w.spinnerPos.value

    @property
    def side(self):
        return int(self.w.side.get())

    @property
    def axis(self):
        return ['x', 'y'][int(self.w.axis.get())]

    @property
    def direction(self):
        return self.w.shiftDirection.get()

    @property
    def delta(self):
        return self.w.spinnerDelta.value

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

        self.drawPreview(previewGlyph, s)

    # -------
    # methods
    # -------

    def drawPreview(self, glyph, scale):

        ctx.save()

        # draw glyph
        ctx.fill(*self.previewFillColor)
        ctx.stroke(*self.previewStrokeColor)
        ctx.strokeWidth(self.previewStrokeWidth * scale)
        ctx.drawGlyph(glyph)

        # draw position
        if self.axis == 'y':
            x1, x2 = -10000, 10000
            y1 = y2 = self.position
        else:
            x1 = x2 = self.position
            y1, y2 = -10000, 10000
        ctx.lineDash(self.previewStrokeWidth * scale, self.previewStrokeWidth * scale)
        ctx.line((x1, y1), (x2, y2))

        # done
        ctx.restore()

    def makeGlyph(self, glyph, preview=False):
        if preview:
            glyph = glyph.copy()
        # flip shift direction
        delta = self.delta
        if not self.direction:
            delta *= -1.0
        # select points
        selectPointsLine(glyph, self.position, axis=self.axis, side=self.side)
        # move points
        shiftSelectedPoints(glyph, delta, axis=self.axis)
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

        sides = ['left', 'right'] if self.axis == 'x' else ['down', 'up']
        directions = ['-', '+']

        if self.verbose:
            print('moving selected points:\n')
            print('\tposition: %s'  % self.position)
            print('\taxis: %s'      % self.axis)
            print('\tside: %s'      % sides[self.side])
            print('\tdistance: %s'  % self.delta)
            print('\tdirection: %s' % directions[self.direction])
            print()
            print('\t', end='')
            print(' '.join(glyphNames), end='\n')

        # ----------------
        # transform glyphs
        # ----------------

        for glyphName in glyphNames:
            g = font[glyphName]
            g.prepareUndo('move glyphs')
            self.makeGlyph(g)
            g.changed()
            g.performUndo()

        # done
        font.changed()
        print('\n...done.\n')

# -------
# testing
# -------

if __name__ == "__main__":

    ShiftPointsDialog()
