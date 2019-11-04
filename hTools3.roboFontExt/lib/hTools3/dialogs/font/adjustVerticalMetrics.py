# coding: utf-8

from __future__ import print_function

from vanilla import Box, TextBox
from mojo.roboFont import CurrentFont, CurrentGlyph, version
from mojo.UI import SliderEditStepper
from hTools3.dialogs import hDialog
from hTools3.modules.fontutils import getFontID

class AdjustVerticalMetricsDialog(hDialog):

    '''
    A dialog to adjust a font’s vertical metrics interactively using sliders.

    '''

    title = "vertical metrics"
    key = '%s.font.verticalMetrics' % hDialog.key
    windowType = 0
    col1 = 80
    vMetrics = ['xHeight', 'ascender', 'descender', 'capHeight']

    def __init__(self):
        self.font = self.getCurrentFont()
        if not self.font:
            return

        self.height  = self.textHeight * len(self.vMetrics)
        self.height += self.textHeight * 1.2
        self.height += self.padding * (len(self.vMetrics) + 2)
        self.width  *= 3
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        self.w.box = Box((x, y, -p, self.textHeight * 1.2))
        self.w.box.text = TextBox(
                (5, 0, -p, self.textHeight),
                '',
                sizeStyle=self.sizeStyle)

        x2 = x + self.col1
        y += self.textHeight * 1.2 + p
        self.controls = {}
        for vMetric in self.vMetrics:
            self.controls[vMetric] = {}
            self.controls[vMetric]['label'] = TextBox(
                (x, y, self.col1, self.textHeight),
                vMetric,
                sizeStyle=self.sizeStyle)
            self.controls[vMetric]['slider'] = SliderEditStepper(
                (x2, y, -p, self.textHeight),
                value=1,
                minValue=1,
                maxValue=1000,
                callback=self.setVMetricsCallback,
                sizeStyle=self.sizeStyle)
            y += self.textHeight + p

        for vMetric in self.controls.keys():
            setattr(self.w, '%sLabel'  % vMetric, self.controls[vMetric]['label'])
            setattr(self.w, '%sSlider' % vMetric, self.controls[vMetric]['slider'])

        self.loadFontValues()
        self.w.open()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def xHeight(self):
        return int(self.controls['xHeight']['slider'].get())

    @property
    def ascender(self):
        return int(self.controls['ascender']['slider'].get())

    @property
    def descender(self):
        return int(self.controls['descender']['slider'].get())

    @property
    def capHeight(self):
        return int(self.controls['capHeight']['slider'].get())

    # -------
    # methods
    # -------

    def loadFontValues(self):
        if not self.font:
            return
        self.w.box.text.set(getFontID(self.font))
        for vMetric in self.vMetrics:
            value = abs(int(getattr(self.font.info, vMetric)))
            slider = self.controls[vMetric]['slider']
            slider.set(value)

    # ---------
    # callbacks
    # ---------

    def setVMetricsCallback(self, sender):
        if not self.font:
            return
        for vMetric in self.vMetrics:
            value = getattr(self, vMetric)
            if vMetric == 'descender':
                value = -value
            setattr(self.font.info, vMetric, value)

# -------
# testing
# -------

if __name__ == '__main__':

    AdjustVerticalMetricsDialog()
