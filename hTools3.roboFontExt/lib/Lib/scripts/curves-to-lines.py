from fontTools.pens.basePen import AbstractPen

class LinePen(AbstractPen):

    def __init__(self, otherPen):
        self._lastPt = None
        self.otherPen = otherPen

    def moveTo(self, pt):
        self._lastPt = pt
        self.otherPen.moveTo(pt)

    def lineTo(self, pt, smooth=False):
        self.otherPen.lineTo(pt)
        self._lastPt = pt

    def curveTo(self, pt1, pt2, pt3):
        self.otherPen.lineTo(pt3)
        self._lastPt = pt3

    def qCurveTo(self, *points):
        self.otherPen.lineTo(points[-1])
        self._lastPt = points[-1]

    def closePath(self):
        self.otherPen.closePath()

    def endPath(self):
        self.otherPen.endPath()

    def addComponent(self, glyphName, transformation):
        self.otherPen.addComponent(glyphName, transformation)

def lineGlyph(aGlyph):
    from fontTools.pens.recordingPen import RecordingPen
    recorder = RecordingPen()
    filterPen = LinePen(recorder)
    aGlyph.draw(filterPen)
    aGlyph.clear()
    recorder.replay(aGlyph.getPen())
    return aGlyph

g = CurrentGlyph()
lineGlyph(g)
