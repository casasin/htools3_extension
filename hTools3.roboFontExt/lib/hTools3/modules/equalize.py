from hTools3.extras.equalize import *

def equalizeCurves(glyph, roundPos=False):
    '''
    Balance handles of all contours in glyph.

    '''
    for cIndex, contour in enumerate(glyph.contours):
        for sIndex, segment in enumerate(contour.segments):
            if segment.type == "curve":
                # first pt is last pt of previous segment
                p0 = contour[sIndex-1][-1]
                if len(segment.points) == 3:
                    p1, p2, p3 = segment.points
                    p1, p2 = eqBalance(p0, p1, p2, p3)
                    if roundPos:
                        p1.round()
                        p2.round()

if __name__ == '__main__':

    glyph = CurrentGlyph()
    glyph.prepareUndo("equalize curves")
    equalizeCurves(glyph)
    glyph.changed()
    glyph.performUndo()
