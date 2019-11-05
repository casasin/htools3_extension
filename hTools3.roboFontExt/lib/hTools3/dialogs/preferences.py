# coding: utf-8

from __future__ import print_function

from importlib import reload
import hTools3.dialogs
reload(hTools3.dialogs)

from vanilla import TextBox, ColorWell, Slider, CheckBox
from mojo.UI import UpdateCurrentGlyphView
from hTools3.dialogs import hDialog
from hTools3.modules.color import rgbToNSColor, nsColorToRGB

class PreferencesDialog(hDialog):

    '''
    A dialog to edit global hTools3 settings.

    ::

        from hTools3.dialogs.preferences import PreferencesDialog
        PreferencesDialog()

    '''

    title = 'settings'
    key = '%s.preferences' % hDialog.key

    def __init__(self):
        self.height  = self.buttonHeight * 2
        self.height += self.textHeight * 5
        self.height += self.padding * 5
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        self.w.previewFillColorLabel = TextBox(
                (x, y, -p, self.textHeight),
                'fill color',
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.previewFillColor = ColorWell(
                (x, y, -p, self.buttonHeight),
                color=rgbToNSColor(self.previewFillColor),
                callback=self.savePreviewFillColorCallback)

        y += self.buttonHeight + p
        self.w.previewStrokeColorLabel = TextBox(
                (x, y, -p, self.textHeight),
                'stroke color',
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.previewStrokeColor = ColorWell(
                (x, y, -p, self.buttonHeight),
                color=rgbToNSColor(self.previewStrokeColor),
                callback=self.saveStrokeColorCallback)

        y += self.buttonHeight + p
        self.w.previewStrokeWidthLabel = TextBox(
                (x, y, -p, self.textHeight),
                'stroke width',
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.previewStrokeWidth = Slider(
                (x, y, -p, self.textHeight),
                value=self.previewStrokeWidth,
                minValue=0,
                maxValue=5,
                tickMarkCount=6,
                stopOnTickMarks=True,
                callback=self.savePreviewStrokeWidthCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.verbose = CheckBox(
                (x, y, -p, self.textHeight),
                "verbose",
                value=self.verbose,
                callback=self.saveVerboseCallback,
                sizeStyle=self.sizeStyle)

        self.w.open()

    # -------------
    # dynamic attrs
    # -------------

    # ...

    # ---------
    # callbacks
    # ---------

    def savePreviewFillColorCallback(self, sender):
        color = sender.get()
        self.previewFillColor = color
        self.updatePreview()

    def saveStrokeColorCallback(self, sender):
        color = sender.get()
        self.previewStrokeColor = color
        self.updatePreview()

    def savePreviewStrokeWidthCallback(self, sender):
        value = sender.get()
        self.previewStrokeWidth = int(value)
        self.updatePreview()

    def saveVerboseCallback(self, sender):
        value = sender.get()
        self.verbose = value
        self.updatePreview()

    # -------
    # methods
    # -------

    def updatePreview(self):
        UpdateCurrentGlyphView()

# -------
# testing
# -------

if __name__ == "__main__":

    PreferencesDialog()
