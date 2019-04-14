# coding: utf-8

from __future__ import print_function

from importlib import reload
import hTools3.dialogs
reload(hTools3.dialogs)

from defconAppKit.windows.baseWindow import BaseWindowController
from mojo.UI import UpdateCurrentGlyphView
from mojo.events import addObserver, removeObserver
from hTools3.dialogs import hDialog

class GlyphsDialogBase(hDialog, BaseWindowController):

    '''
    A Base object for tools which do something to selected glyphs in the current font.

    '''

    title = None
    key = '%s.glyphs' % hDialog.key

    def initGlyphsWindowBehaviour(self):
        '''
        Initialize basic window behavior.

        '''
        self.setUpBaseWindowBehavior()
        addObserver(self, "backgroundPreview", "drawBackground")
        addObserver(self, "backgroundPreview", "drawPreview")
        UpdateCurrentGlyphView()

    # ---------
    # callbacks
    # ---------

    def windowCloseCallback(self, sender):
        '''
        Removes observers from the dialog after the window is closed.

        '''
        super().windowCloseCallback(sender)
        removeObserver(self, "drawBackground")
        removeObserver(self, "drawPreview")

    def updatePreviewCallback(self, sender):
        UpdateCurrentGlyphView()

    def applyCallback(self, sender):
        self.apply()

    # ---------
    # observers
    # ---------

    def backgroundPreview(self, notification):
        '''
        Draw a preview of the current settings in the background of the Glyph View.

        '''
        pass

    def backgroundPreviewPlain(self, notification):
        pass

    # -------
    # methods
    # -------

    def makeGlyph(self, glyph, *args):
        '''
        Transform an input glyph to make a new glyph.

        Args:
            glyph (RGlyph): An input glyph.

        Returns:
            An output glyph (RGlyph).

        '''
        pass

    def apply(self):
        '''
        Apply actions to selected glyphs.

        '''
        pass
