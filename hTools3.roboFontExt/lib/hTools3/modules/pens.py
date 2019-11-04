import os
from fontTools.pens.basePen import BasePen

class LinePen(BasePen):

    '''A pen which converts curve segments into line segments.'''

    def __init__(self, otherPen):
        BasePen.__init__(self, {})
        self.otherPen = otherPen
        self.currentPt = None
        self.firstPt = None

    def _moveTo(self, pt):
        self.otherPen.moveTo(pt)
        self.currentPt = pt
        self.firstPt = pt

    def _lineTo(self, pt):
        self.otherPen.lineTo(pt)
        self.currentPt = pt

    def _curveToOne(self, pt1, pt2, pt3):
        self.otherPen.lineTo(pt3)
        self.currentPt = pt3

    def _closePath(self):
        self.lineTo(self.firstPt)
        self.otherPen.closePath()
        self.currentPt = None

    def _endPath(self):
        self.otherPen.endPath()
        self.currentPt = None

    def addComponent(self, glyphName, transformation):
        self.otherPen.addComponent(glyphName, transformation)
