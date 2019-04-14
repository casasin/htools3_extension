import os
import drawBot
from random import random
from mojo.roboFont import OpenFont
from hTools3.objects.hproject import hProject

class EGlyph:

    project = hProject('/Volumes/gf_bkp_3/_fonts/gridfonts/Elementar')
    scale   = 0.12
    padding = 1

    heights     = []
    weights     = []
    widths      = []
    resolutions = []

    def getFont(self, EName):
        fontName = '%02d-%s-%s' % EName
        ufoPath = self.project.fonts[fontName]
        return OpenFont(ufoPath, showInterface=False)

    def draw(self, pos, txt):

        x, y = pos
        gridSize = self.project.lib['gridSize']

        res = [1, 2, 4, 8][0]

        for char in txt:
            glyphName = char

            drawBot.newPage(1000, 1000)
            drawBot.translate(x, y)
            drawBot.scale(self.scale)

            X, Y = x, y

            for ht in self.heights:
                X = x
                drawBot.save()
                h = ht * gridSize
                for wt in self.weights:
                    for i, wd in enumerate(self.widths):

                        EName = ht, wt, wd
                        font = self.getFont(EName)

                        drawBot.stroke(1, 0, 0)
                        drawBot.line((0, 0), (0, h))
                        drawBot.stroke(None)

                        color = 0, 0, 1
                        if len(self.resolutions) > 1:
                            alpha = 1.0 / len(self.resolutions)
                            color += (alpha,)

                        drawBot.fill(*color)
                        for res in self.resolutions:
                            g = font[glyphName].getLayer(str(res))
                            yBaseline = abs(font.info.descender)
                            with drawBot.savedState():
                                drawBot.translate(0, yBaseline)
                                drawBot.drawGlyph(g)

                        drawBot.translate(g.width + self.padding * gridSize, 0)

                        if i == len(self.widths) - 1:
                            drawBot.stroke(1, 0, 0)
                            drawBot.line((0, 0), (0, h))
                            drawBot.stroke(None)

                drawBot.restore()
                drawBot.translate(0, h + self.padding * gridSize)
