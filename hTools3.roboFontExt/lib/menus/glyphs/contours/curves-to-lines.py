# menuTitle : curves to lines

from importlib import reload
import hTools3.modules.pens
reload(hTools3.modules.pens)

from hTools3.modules.pens import LinePen

def curvesToLines(glyph):
    hasCurves = any([(True if s.type == 'curve' else False) for c in glyph for s in c])
    if not hasCurves:
        return
    g = RGlyph()
    drawPen = g.getPen()
    linePen = LinePen(drawPen)
    glyph.draw(linePen)
    glyph.clearContours()
    glyph.appendGlyph(g)

g = CurrentGlyph()
if g is not None:
    g.prepareUndo()
    curvesToLines(g)
    g.performUndo()
