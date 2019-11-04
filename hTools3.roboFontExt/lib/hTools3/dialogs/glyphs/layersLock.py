# coding: utf-8

from vanilla import HUDFloatingWindow, SquareButton, CheckBox
from defconAppKit.windows.baseWindow import BaseWindowController
from mojo import drawingTools as ctx
from mojo.roboFont import CurrentFont, CurrentGlyph
from mojo.events import addObserver, removeObserver
from mojo.UI import UpdateCurrentGlyphView, getDefault
from hTools3.dialogs import hDialog

class LockLayerWidthsDialog(hDialog, BaseWindowController):

    title = 'widths'
    key = '%s.glyphs.layers.lock' % hDialog.key

    def __init__(self):
        self.height  = self.textHeight * 2
        self.height += self.buttonHeight * 2
        self.height += self.padding * 4 - 3
        self.w = self.window((self.width, self.height), title=self.title)

        x = y = p = self.padding
        self.w.lockLayers = SquareButton(
                (x, y, -p, self.buttonHeight),
                'lock',
                callback=self.lockGlyphsCallback,
                sizeStyle=self.sizeStyle)

        y += self.buttonHeight + p
        self.w.unlockLayers = SquareButton(
                (x, y, -p, self.buttonHeight),
                'unlock',
                callback=self.unlockGlyphsCallback,
                sizeStyle=self.sizeStyle)

        y += self.buttonHeight + p
        self.w.currentGlyph = CheckBox(
                (x, y, -p, self.textHeight),
                'current glyph',
                value=True,
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.fontSelection = CheckBox(
                (x, y, -p, self.textHeight),
                'font selection',
                value=True,
                sizeStyle=self.sizeStyle)

        self.setUpBaseWindowBehavior()
        addObserver(self, "drawCallback", "draw")
        addObserver(self, "drawCallback", "spaceCenterDraw")

        self.w.open()

    # ---------
    # callbacks
    # ---------

    def windowCloseCallback(self, sender):
        super().windowCloseCallback(sender)
        removeObserver(self, "draw")
        removeObserver(self, "spaceCenterDraw")

    def drawCallback(self, notification):
        glyph = notification['glyph']
        scale = notification['scale']

        font = glyph.font

        # get glyph lock status
        lockStatus = False
        if self.key in font.lib:
            if glyph.name in font.lib[self.key]:
                lockStatus = font.lib[self.key][glyph.name]

        # copy width to all other layers
        if lockStatus:
            for layerName in font.layerOrder:
                layerGlyph = glyph.getLayer(layerName)
                layerGlyph.width = glyph.width

        # draw lock status in canvas
        if not 'spaceCenter' in notification:
            if lockStatus:
                lockStatusText = '🔒'
            else:
                lockStatusText = '🔓'
            ctx.save()
            ctx.fontSize(24 * scale)
            ctx.text(lockStatusText, (glyph.width, 0))
            ctx.restore()

    def lockGlyphsCallback(self, sender):
        self.setLockStatus(True)
        UpdateCurrentGlyphView()

    def unlockGlyphsCallback(self, sender):
        self.setLockStatus(False)
        UpdateCurrentGlyphView()

    # -------
    # methods
    # -------

    def setLockStatus(self, value):
        font = CurrentFont()
        if not font:
            return

        glyphNames = []

        # get current glyph
        if self.w.currentGlyph.get():
            g = CurrentGlyph()
            if g is not None:
                glyphNames += [g.name]

        # get font selection
        if self.w.fontSelection.get():
            glyphNames += font.selectedGlyphNames

        # remove duplicates and sort
        glyphNames = sorted(list(set(glyphNames)))

        # get glyphName:lockStatus dict
        lockGlyphsDict = {}
        if self.key in font.lib:
            lockGlyphsDict = font.lib[self.key]

        # set lock status for selected glyphs
        for glyphName in glyphNames:
            if self.verbose:
                if value:
                    print('locking layer widths (%s)...' % glyphName)
                else:
                    print('unlocking layer widths (%s)...' % glyphName)
            lockGlyphsDict[glyphName] = value

        # save glyph lock dict in font lib
        font.lib[self.key] = lockGlyphsDict

# -------
# testing
# -------

if __name__ == '__main__':

    D = LockLayerWidthsDialog()
