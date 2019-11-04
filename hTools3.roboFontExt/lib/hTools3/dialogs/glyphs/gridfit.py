# coding: utf-8

from __future__ import print_function

from importlib import reload
import hTools3.dialogs.glyphs.base
reload(hTools3.dialogs.glyphs.base)

from vanilla import CheckBox, SquareButton
from mojo import drawingTools as ctx
from mojo.UI import getDefault, setDefault, getGlyphViewDisplaySettings, setGlyphViewDisplaySettings, UpdateCurrentGlyphView
from mojo.events import removeObserver
from mojo.roboFont import RGlyph
from lib.tools.notifications import PostNotification
from defcon import Glyph, registerRepresentationFactory, unregisterRepresentationFactory
from hTools3.dialogs.glyphs.base import GlyphsDialogBase
from hTools3.dialogs.misc.spinner import Spinner
from hTools3.modules.glyphutils import roundPoints, roundBPoints, roundMargins, roundWidth, roundAnchors, roundComponents

def gridfitGlyphFactory(glyph, gridsize, points=False, bPoints=True, margins=False, width=True, anchors=False, components=False):

    glyph = RGlyph(glyph).copy()

    if points:
        roundPoints(glyph, gridsize)
    else:
        if bPoints:
            roundBPoints(glyph, gridsize)

    if margins:
        roundMargins(glyph, gridsize)
    else:
        if width:
            roundWidth(glyph, gridsize)

    if anchors:
        roundAnchors(glyph, gridsize)

    if components:
        roundComponents(glyph, gridsize)

    return glyph

class RoundToGridDialog(GlyphsDialogBase):

    '''
    A dialog to round points, metrics, anchors and components in the selected glyphs to a grid.

    .. code-block:: python

        from hTools3.dialogs.glyphs.gridfit import RoundToGridDialog
        RoundToGridDialog()

    '''

    title = 'gridfit'
    key = '%s.gridfit' % GlyphsDialogBase.key
    settings = {
        'gridSize'   : 30,
        'bPoints'    : True,
        'points'     : False,
        'margins'    : False,
        'width'      : True,
        'anchors'    : False,
        'components' : False,
        'layers'     : False,
        'previewPointRadius' : 5,
    }

    def __init__(self):
        self.height  = self.spinnerHeight
        self.height += self.textHeight * 8
        self.height += self.padding * 5
        self.height += self.buttonHeight
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        self.w.gridSize = Spinner(
                (x, y),
                default=self.settings['gridSize'],
                integer=True,
                callback=self.gridSizeCallback,
                label='grid')

        y += self.w.gridSize.height + p
        self.w.bPoints = CheckBox(
                (x, y, -p, self.textHeight),
                "bPoints",
                value=self.settings['bPoints'],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.points = CheckBox(
                (x, y, -p, self.textHeight),
                "points",
                value=self.settings['points'],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.margins = CheckBox(
                (x, y, -p, self.textHeight),
                "margins",
                value=self.settings['margins'],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.width = CheckBox(
                (x, y, -p, self.textHeight),
                "width",
                value=self.settings['width'],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.anchors = CheckBox(
                (x, y, -p, self.textHeight),
                "anchors",
                value=self.settings['anchors'],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.components = CheckBox(
                (x, y, -p, self.textHeight),
                "components",
                value=self.settings['components'],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
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

        y += self.textHeight
        self.w.showGrid = CheckBox(
                (x, y, -p, self.textHeight),
                "show grid",
                value=True,
                callback=self.showGridCallback,
                sizeStyle=self.sizeStyle)

        self.setGridSize(self.settings['gridSize'])
        self.toggleGrid(True)

        self.initGlyphsWindowBehaviour()

        registerRepresentationFactory(Glyph, "%s.preview" % self.key, gridfitGlyphFactory)

        self.w.open()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def gridSize(self):
        '''
        The size of the grid as set by the user.

        '''
        return abs(self.w.gridSize.value)

    @property
    def bPoints(self):
        '''
        A boolean indicating if bPoints should be rounded to grid.

        '''
        return self.w.bPoints.get()

    @property
    def points(self):
        '''
        A boolean indicating if points should be rounded to grid.

        '''
        return self.w.points.get()

    @property
    def margins(self):
        '''
        A boolean indicating if the glyph margins should be rounded to grid.

        '''
        return self.w.margins.get()

    @property
    def glyphWidth(self):
        '''
        A boolean indicating if the glyph width should be rounded to grid.

        '''
        return self.w.width.get()

    @property
    def anchors(self):
        '''
        A boolean indicating if anchor positions should be rounded to grid.

        '''
        return self.w.anchors.get()

    @property
    def components(self):
        '''
        A boolean indicating if component positions should be rounded to grid.

        '''
        return self.w.components.get()

    # ---------
    # callbacks
    # ---------

    def gridSizeCallback(self, sender):
        self.setGridSize(self.gridSize)
        UpdateCurrentGlyphView()

    def showGridCallback(self, sender):
        value = sender.get()
        self.toggleGrid(value)

    def windowCloseCallback(self, sender):
        '''
        Removes observers and representation factories after the window is closed.

        '''
        super().windowCloseCallback(sender)
        removeObserver(self, "drawBackground")
        removeObserver(self, "drawPreview")
        unregisterRepresentationFactory(Glyph, "%s.preview" % self.key)

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

        if self.gridSize == 0:
            return

        # get preview
        previewGlyph = g.getRepresentation("%s.preview" % self.key, gridsize=self.gridSize, points=self.points, bPoints=self.bPoints, margins=self.margins, width=self.glyphWidth, anchors=self.anchors, components=self.components)

        # draw preview
        if notification['notificationName'] == 'drawBackground':
            self.drawPreview(previewGlyph, s)
        else:
            self.drawPreview(previewGlyph, s, plain=True)

    # -------
    # methods
    # -------

    def setGridSize(self, gridSize):
        '''
        Apply the given gridsize by saving it to the preferences.

        '''
        if not gridSize > 0:
            return
        setDefault("glyphViewGridx", gridSize)
        setDefault("glyphViewGridy", gridSize)
        PostNotification("doodle.preferencesChanged")

    def toggleGrid(self, value):
        settings = getGlyphViewDisplaySettings()
        settings['Grid'] = value
        setGlyphViewDisplaySettings(settings)

    def drawPreview(self, glyph, previewScale, plain=False):

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

        ctx.drawGlyph(glyph)

        if not plain:
            r = self.settings['previewPointRadius'] * previewScale
            ctx.fill(None)

            # draw points
            if self.points:
                for contour in glyph.contours:
                    for pt in contour.points:
                        ctx.oval(pt.x - r, pt.y - r, r * 2, r * 2)
            else:
                # draw bPoints
                if self.bPoints:
                    for contour in glyph.contours:
                        for bPoint in contour.bPoints:
                            x, y = bPoint.anchor
                            ctx.oval(x - r, y - r, r * 2, r * 2)

            # draw width
            if self.glyphWidth or self.margins:
                y1 = -10000
                y2 = 10000
                ctx.save()
                ctx.lineDash(self.previewStrokeWidth * previewScale, self.previewStrokeWidth * previewScale)
                ctx.line((glyph.width, y1), (glyph.width, y2))
                ctx.restore()

            # draw anchors
            if self.anchors:
                ctx.save()
                for anchor in glyph.anchors:
                    x, y = anchor.x, anchor.y
                    r = self.previewOriginRadius * previewScale
                    ctx.fill(None)
                    ctx.line((x - r, y), (x + r, y))
                    ctx.line((x, y - r), (x, y + r))
                    ctx.oval(x - r, y - r, r * 2, r * 2)
                ctx.restore()

        ctx.restore()

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
            print('gridfitting glyphs:\n')
            print('\tgridize: %s' % self.gridSize)
            print()
            print('\t', end='')
            print(' '.join(glyphNames), end='\n')

        # ----------------
        # transform glyphs
        # ----------------

        for glyphName in glyphNames:
            g = font[glyphName]
            result = g.getRepresentation("%s.preview" % self.key, gridsize=self.gridSize, points=self.points, bPoints=self.bPoints, margins=self.margins, width=self.glyphWidth, anchors=self.anchors, components=self.components)
            g.prepareUndo('gridfit')
            g.clear()
            g.appendGlyph(result)
            g.changed()
            g.performUndo()

        # done
        font.changed()
        if self.verbose:
            print('\n...done.\n')

# --------
# testing
# -------

if __name__ == "__main__":

    RoundToGridDialog()