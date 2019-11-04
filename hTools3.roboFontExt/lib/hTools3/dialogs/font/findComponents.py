# -*- coding: utf-8 -*-
from mojo.roboFont import version
if version >= "3.0":
    from importlib import reload

import moshikTools.modules.components
reload(moshikTools.modules.components)

from moshikTools.modules.components import findComposedGlyphs

from vanilla import FloatingWindow, EditText, List, SquareButton
from mojo.UI import OpenGlyphWindow
from mojo.roboFont import CurrentFont

class FindComponentsTool(object):

    width        = 246
    height       = 320
    padding      = 10
    textHeight   = 20
    buttonHeight = 27

    def __init__(self):
        self.w = FloatingWindow(
                (self.width, self.height),
                "Find Components",
                minSize=(self.width, self.height))
        x = y = p = self.padding
        self.w.baseGlyph = EditText(
                (x, y, -p, self.textHeight),
                'a',
                sizeStyle='small')
        y += self.textHeight + p
        listHeight = -(self.buttonHeight + p*2)
        self.w.composed = List((x, y, -p, listHeight),
                 [],
                 doubleClickCallback=self.selectionCallback,
                 allowsMultipleSelection=False,
                 allowsEmptySelection=False)
        y = -(self.buttonHeight + p)
        self.w.applyButton = SquareButton(
                (x, y, -p, self.buttonHeight),
                'find components',
                sizeStyle='small',
                callback=self.findComponentsCallback)
        # open window
        self.w.open()

    def findComponentsCallback(self, sender):
        f = CurrentFont()
        if f:
            g = self.w.baseGlyph.get()
            composed = findComposedGlyphs(f, g)
            self.w.composed.set(composed)

    def selectionCallback(self, sender):
        f = CurrentFont()
        if f:
            i = self.w.composed.getSelection()[0]
            composed = self.w.composed.get()[i]
            OpenGlyphWindow(glyph=f[composed], newWindow=True)
