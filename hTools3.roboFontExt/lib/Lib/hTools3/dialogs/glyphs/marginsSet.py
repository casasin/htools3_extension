# coding: utf-8

from __future__ import print_function

import math
from vanilla import RadioGroup, SquareButton, CheckBox, EditText
from mojo import drawingTools as ctx
from mojo.tools import IntersectGlyphWithLine
from hTools3.dialogs.glyphs.base import GlyphsDialogBase
from hTools3.dialogs.misc.spinner import Spinner

class SetMarginsDialog(GlyphsDialogBase):

    '''
    A dialog to set the left/right margins of selected glyphs in the current font.

    .. code-block:: python

        from hTools3.dialogs.glyphs.marginsSet import SetMarginsDialog
        SetMarginsDialog()

    '''

    title = 'set margins'
    key = '%s.margins' % GlyphsDialogBase.key
    settings = {
        'left'       : True,
        'leftMode'   : 0,
        'leftValue'  : 100,
        'right'      : True,
        'rightMode'  : 0,
        'rightValue' : 100,
        'beamValue'  : 400,
    }

    #: Modes for setting new margin values.
    modes = [
        'set equal to',
        'increase by',
        'decrease by'
    ]

    def __init__(self):
        self.height  = self.spinnerHeight * 3
        self.height += self.textHeight * 5
        self.height += self.buttonHeight
        self.height += self.padding * 10 - 3
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        self.w.leftMode = RadioGroup(
                (x, y, -p, self.textHeight),
                ['=', '+', '-'],
                sizeStyle=self.sizeStyle,
                callback=self.updatePreviewCallback,
                isVertical=False)
        self.w.leftMode.set(self.settings['leftMode'])

        y += self.textHeight + p
        self.w.leftSpinner = Spinner(
                (x, y),
                default=self.settings['leftValue'],
                integer=True,
                callback=self.updatePreviewCallback,
                label='left')

        y += self.w.leftSpinner.height + p
        self.w.rightMode = RadioGroup(
                (x, y, -p, self.textHeight),
                ['=', '+', '-'],
                sizeStyle=self.sizeStyle,
                callback=self.updatePreviewCallback,
                isVertical=False)
        self.w.rightMode.set(self.settings['rightMode'])

        y += self.textHeight + p
        self.w.rightSpinner = Spinner(
                (x, y),
                default=self.settings['rightValue'],
                integer=True,
                callback=self.updatePreviewCallback,
                label='right')

        y += self.w.rightSpinner.height + p - 1
        self.w.beam = CheckBox(
                (x, y, -p, self.textHeight),
                "use beam",
                value=False,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.beamY = Spinner(
                (x, y),
                default=self.settings['beamValue'],
                integer=True,
                callback=self.updatePreviewCallback,
                label='y beam')

        y += self.w.beamY.height + p
        self.w.leftCheckbox = CheckBox(
                (x, y, self.width * 0.5 - p, self.textHeight),
                "left",
                value=self.settings['left'],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        x += self.width * 0.5 - p
        self.w.rightCheckbox = CheckBox(
                (x, y, self.width * 0.5 - p, self.textHeight),
                "right",
                value=self.settings['right'],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

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
    def left(self):
        '''Toggle set left margin on/off.'''
        return bool(self.w.leftCheckbox.get())

    @property
    def leftValue(self):
        '''Current spinner value for left margin.'''
        return self.w.leftSpinner.value

    @property
    def leftMode(self):
        '''Current select mode for left margin.'''
        return self.w.leftMode.get()

    @property
    def right(self):
        '''Toggle set right margin on/off.'''
        return bool(self.w.rightCheckbox.get())

    @property
    def rightValue(self):
        '''Current spinner value for right margin.'''
        return self.w.rightSpinner.value

    @property
    def rightMode(self):
        '''Current select mode for right margin.'''
        return self.w.rightMode.get()

    @property
    def beam(self):
        '''Toggle the measurement beam on/off.'''
        return bool(self.w.beam.get())

    @property
    def beamY(self):
        '''The y-position of the measurement beam.'''
        return self.w.beamY.value

    # ---------
    # observers
    # ---------

    def backgroundPreview(self, notification):
        '''
        Draw a preview of the new margins in the background.

        '''
        g = notification['glyph']
        s = notification['scale']

        # ------------------
        # assert conditions
        # ------------------

        if not self.w.preview.get():
            return

        if not g:
            return

        # skip empty glyphs
        if not g.bounds and not len(g.components):
            return

        # when beam mode is ON:
        # skip glyph if no intersections with beam
        if not self.assertGlyph(g):
            return

        # ------------
        # make preview
        # ------------

        previewGlyph = self.makeGlyph(g, preview=True)

        # ------------
        # draw preview
        # ------------

        self.drawPreview(g, previewGlyph, s)

    # -------
    # methods
    # -------

    def assertGlyph(self, glyph):
        '''
        Check if the glyph is valid for setting margins under the current settings.

        '''
        # exception: if the beam position is too low or too high
        # no margins are returned by the beam even though the glyph is not empty
        # this method is used to double-check each glyph when beam mode is ON
        margins = self.getMargins(glyph)
        if not margins:
            if self.verbose:
                print('WARNING: beam does not intersect with shape in %s.' % glyph.name)
            return False
        else:
            return True

    def getIntersections(self, glyph):
        '''
        Get the intersections between a beam at a given y-position and a glyph’s contours.

        '''
        intersections = sorted(IntersectGlyphWithLine(glyph, ((-10000, self.beamY), (10000, self.beamY)), canHaveComponent=True, addSideBearings=False))
        return intersections[0][0], intersections[-1][0]

    def getMargins(self, glyph):
        '''
        Get the margins of a glyph under the current settings.

        '''
        # use assertMargins(glyph) before calling this method to make sure it will not return `None`
        if self.beam:
            intersections = sorted(IntersectGlyphWithLine(glyph, ((-10000, self.beamY), (10000, self.beamY)), canHaveComponent=True, addSideBearings=False))
            if not len(intersections):
                return
            leftMargin  = intersections[0][0]
            rightMargin = glyph.width - intersections[-1][0]
            return leftMargin, rightMargin
        else:
            return glyph.leftMargin, glyph.rightMargin

    def drawPreview(self, glyph, previewGlyph, previewScale):

        leftDiff = previewGlyph.leftMargin - glyph.leftMargin

        # get italic angle & slant offset
        angle = glyph.font.info.italicAngle

        if angle is None:
            angle = 0

        elif angle != 0:
            try:
                slantOffset = font.lib['com.typemytype.robofont.italicSlantOffset']
            except:
                slantOffset = math.tan(angle * math.pi / 180) * (glyph.font.info.xHeight * 0.5)

        ctx.save()

        # ----------
        # draw glyph
        # ----------

        ctx.save()

        ctx.fill(*self.previewFillColor)
        ctx.stroke(*self.previewStrokeColor)
        ctx.strokeWidth(self.previewStrokeWidth * previewScale)
        ctx.translate(-leftDiff, 0)
        ctx.drawGlyph(previewGlyph)

        # draw margins
        y1, y2 = -10000, 10000

        if self.left:
            x = 0
            ctx.lineDash(self.previewStrokeWidth * previewScale, self.previewStrokeWidth * previewScale)
            ctx.line((x, y1), (x, y2))
            if angle != 0:
                ctx.save()
                ctx.skew(-glyph.font.info.italicAngle, 0)
                ctx.translate(slantOffset, 0)
                ctx.line((x, y1), (x, y2))
                ctx.restore()

        if self.right:
            x = previewGlyph.width
            ctx.lineDash(self.previewStrokeWidth * previewScale, self.previewStrokeWidth * previewScale)
            ctx.line((x, y1), (x, y2))
            if angle != 0:
                ctx.save()
                ctx.skew(-glyph.font.info.italicAngle, 0)
                ctx.translate(slantOffset, 0)
                ctx.line((x, y1), (x, y2))
                ctx.restore()

        ctx.restore()

        # ---------
        # draw beam
        # ---------

        if self.beam:
            x1, x2 = -10000, 10000
            ctx.save()
            ctx.stroke(*self.previewStrokeColor)
            ctx.strokeWidth(self.previewStrokeWidth * previewScale)
            ctx.lineDash(self.previewStrokeWidth * previewScale, self.previewStrokeWidth * previewScale)
            ctx.line((x1, self.beamY), (x2, self.beamY))

            # draw intersections
            r = self.previewOriginRadius * previewScale
            y = self.beamY
            ctx.lineDash(None)
            ctx.fill(None)
            for i, x in enumerate(self.getIntersections(glyph)):
                if (i == 0 and self.left) or (i == 1 and self.right):
                    ctx.line((x - r, y), (x + r, y))
                    ctx.line((x, y - r), (x, y + r))
                    ctx.oval(x - r, y - r, r * 2, r * 2)
            ctx.restore()

        # done
        ctx.restore()

    def makeGlyph(self, glyph, preview=False):

        if preview:
            glyph = glyph.copy()

        # -----------
        # get margins
        # -----------

        oldLeft, oldRight = glyph.leftMargin, glyph.rightMargin
        beamLeft, beamRight = self.getMargins(glyph)

        # ---------------
        # set left margin
        # ---------------

        if self.left:

            if self.leftMode == 1: # increase
                newLeft = oldLeft + self.leftValue

            elif self.leftMode == 2: # decrease
                newLeft = oldLeft - self.leftValue

            else: # equal to
                newLeft = self.leftValue

            if self.beam:
                newLeft -= beamLeft - oldLeft

            glyph.leftMargin = newLeft
            glyph.changed()

        # ----------------
        # set right margin
        # ----------------

        if self.right:

            if self.rightMode == 1: # increase
                newRight = oldRight + self.rightValue

            elif self.rightMode == 2: # decrease
                newRight = oldRight - self.rightValue

            else: # equal to
                newRight = self.rightValue

            if self.beam:
                newRight -= beamRight - oldRight

            glyph.rightMargin = newRight
            glyph.changed()

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
            print('setting margins:\n')
            print('\tleft: %s %s (%s)'  % (self.modes[self.leftMode],  self.leftValue, self.left))
            print('\tright: %s %s (%s)' % (self.modes[self.rightMode], self.rightValue, self.right))
            print('\tbeam: %s (%s)' % (self.beamY, ['OFF', 'ON'][int(self.beam)]))
            print()
            print('\t', end='')
            print(' '.join(glyphNames), end='\n')

        # ----------------
        # transform glyphs
        # ----------------

        for glyphName in glyphNames:
            g = font[glyphName]
            if not self.assertGlyph(g):
                continue
            g.prepareUndo('set margins')
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

    SetMarginsDialog()
