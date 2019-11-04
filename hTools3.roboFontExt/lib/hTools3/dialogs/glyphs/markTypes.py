# coding: utf-8

from __future__ import print_function

from vanilla import CheckBox, SquareButton, ColorWell
from mojo.roboFont import CurrentFont
from hTools3.dialogs import hDialog
from hTools3.modules.color import rgbToNSColor, nsColorToRGB
from hTools3.modules.fontutils import markGlyphs, findMarkColor

def markGlyphType(g, colorsDict):
    # contours only
    if len(g.contours) and not len(g.components):
        g.markColor = colorsDict['contours']
    # components only
    elif not len(g.contours) and len(g.components):
        g.markColor = colorsDict['components']
    # contours and components
    elif len(g.contours) and len(g.components):
        g.markColor = colorsDict['contoursComponents']
    # empty
    else:
        g.markColor = colorsDict['empty']

class MarkGlyphTypesDialog(hDialog):

    title = 'mark'

    # key = hDialog.key
    # key += 'glyphs.markTypes'

    settings = {
        'contours'           : (0, 1, 0, 0.5), # green
        'components'         : (0, 0, 1, 0.5), # blue
        'contoursComponents' : (1, 0, 0, 0.5), # red
        'empty'              : (1, 1, 0, 0.5), # yellow
    }

    def __init__(self):
        self.height  = self.buttonHeight * 5
        self.height += self.padding * 8
        self.height += self.textHeight * 4
        self.width  *= 1.35
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        self.w.labelContours = CheckBox(
                (x, y, -self.padding, self.textHeight),
                'contours only',
                value=True,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p * .5
        self.w.colorContours = ColorWell(
                (x, y, -self.padding, self.buttonHeight),
                color=rgbToNSColor(self.settings['contours']))

        y += self.buttonHeight + self.padding
        self.w.labelComponents = CheckBox(
                (x, y, -self.padding, self.textHeight),
                'components only',
                value=True,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p * .5
        self.w.colorComponents = ColorWell(
                (x, y, -self.padding, self.buttonHeight),
                color=rgbToNSColor(self.settings['components']))

        y += self.buttonHeight + self.padding
        self.w.labelContoursComponents = CheckBox(
                (x, y, -self.padding, self.textHeight),
                'contours & components',
                value=True,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p * .5
        self.w.colorContoursComponents = ColorWell(
                (x, y, -self.padding, self.buttonHeight),
                color=rgbToNSColor(self.settings['contoursComponents']))

        y += self.buttonHeight + self.padding
        self.w.labelEmpty = CheckBox(
                (x, y, -self.padding, self.textHeight),
                'empty glyphs',
                value=True,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p * .5
        self.w.colorEmpty = ColorWell(
                (x, y, -self.padding, self.buttonHeight),
                color=rgbToNSColor(self.settings['empty']))

        y += self.buttonHeight + self.padding
        self.w.applyButton = SquareButton(
                (x, y, -self.padding, self.buttonHeight),
                "apply",
                callback=self.markGlyphsCallback,
                sizeStyle=self.sizeStyle)

        self.w.open()

    def markGlyphsCallback(self, sender):

        font = self.getCurrentFont()
        if not font:
            return

        colorsDict = {
            'contours'           : nsColorToRGB(self.w.colorContours.get()),
            'components'         : nsColorToRGB(self.w.colorComponents.get()),
            'contoursComponents' : nsColorToRGB(self.w.colorContoursComponents.get()),
            'empty'              : nsColorToRGB(self.w.colorEmpty.get()),
        }

        print('marking glyph types in font %s %s...' % (font.info.familyName, font.info.styleName))

        for g in font:
            markGlyphType(g, colorsDict)

        print('...done.\n')

if __name__ == '__main__':

    MarkGlyphTypesDialog()
