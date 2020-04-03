from importlib import reload
import hTools3.dialogs
reload(hTools3.dialogs)

from vanilla import TextBox, ColorWell, Slider, CheckBox, Group
from mojo.UI import UpdateCurrentGlyphView, AccordionView
from hTools3.dialogs import hDialog
from hTools3.modules.color import rgbToNSColor, nsColorToRGB


class PreferencesDialog(hDialog):

    '''
    A dialog to edit global hTools3 settings.

    ::

        from hTools3.dialogs.preferences import PreferencesDialog
        PreferencesDialog()

    '''

    title = 'preferences'
    key = '%s.preferences' % hDialog.key
    windowType = 0

    def __init__(self):
        self.width  *= 1.2
        self.height = 360
        self.w = self.window(
                (self.width, self.height), self.title,
                minSize=(self.width, self.height * 0.75),
                maxSize=(self.width * 1.5, self.height * 2))

        self.initPreviewGroup()
        self.initOptionsGroup()
        self.initAccordionView()

        self.w.open()

    # -------------
    # dynamic attrs
    # -------------

    # ------------
    # initializers
    # ------------

    def initPreviewGroup(self):

        self.previewGroup =  Group((0, 0, -0, -0))

        x = y = p = self.padding
        self.previewGroup.previewFillColorLabel = TextBox(
                (x, y, -p, self.textHeight),
                'fill color',
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.previewGroup.previewFillColor = ColorWell(
                (x, y, -p, self.buttonHeight),
                color=rgbToNSColor(self.previewFillColor),
                callback=self.savePreviewFillColorCallback)

        y += self.buttonHeight + p
        self.previewGroup.previewStrokeColorLabel = TextBox(
                (x, y, -p, self.textHeight),
                'stroke color',
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.previewGroup.previewStrokeColor = ColorWell(
                (x, y, -p, self.buttonHeight),
                color=rgbToNSColor(self.previewStrokeColor),
                callback=self.saveStrokeColorCallback)

        y += self.buttonHeight + p
        self.previewGroup.previewStrokeWidthLabel = TextBox(
                (x, y, -p, self.textHeight),
                'stroke width',
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.previewGroup.previewStrokeWidth = Slider(
                (x, y, -p, self.textHeight),
                value=self.previewStrokeWidth,
                minValue=0,
                maxValue=5,
                tickMarkCount=6,
                stopOnTickMarks=True,
                callback=self.savePreviewStrokeWidthCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.previewGroupHeight = y

    def initOptionsGroup(self):

        self.optionsGroup =  Group((0, 0, -0, -0))

        x = y = p = self.padding
        self.optionsGroup.verbose = CheckBox(
                (x, y, -p, self.textHeight),
                "verbose",
                value=self.verbose,
                callback=self.saveVerboseCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.optionsGroupHeight = y

    def initAccordionView(self):
        descriptions = [
            dict(label="preview",
                view=self.previewGroup,
                size=self.previewGroupHeight,
                collapsed=False,
                canResize=False),
            dict(label="options",
                view=self.optionsGroup,
                size=self.optionsGroupHeight,
                collapsed=False,
                canResize=False),
        ]
        self.w.accordionView = AccordionView((0, 0, -0, -0), descriptions)

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
