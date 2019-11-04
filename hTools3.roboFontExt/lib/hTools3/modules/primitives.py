# coding: utf-8

'''
Helpers for drawing basic geometric shapes with a pen.

'''

#: A constant for drawing circular arcs with beziers.
BEZIER_ARC_CIRCLE = 0.5522847493

def rect(pen, x, y, w, h):
    '''
    Draw a rectangle with a pen object.

    '''
    pen.moveTo((x, y))
    pen.lineTo((x, y + h))
    pen.lineTo((x + w, y + h))
    pen.lineTo((x + w, y))
    pen.closePath()

def oval(pen, x, y, w, h):
    '''
    Draw an oval with a pen object.

    '''
    rx = w * 0.5
    ry = h * 0.5
    bcpx = BEZIER_ARC_CIRCLE * rx
    bcpy = BEZIER_ARC_CIRCLE * ry
    x += rx
    y += ry
    pen.moveTo((x, y + ry))
    pen.curveTo((x + bcpx, y + ry), (x + rx, y + bcpy), (x + rx, y))
    pen.curveTo((x + rx, y - bcpy), (x + bcpx, y - ry), (x, y - ry))
    pen.curveTo((x - bcpx, y - ry), (x - rx, y - bcpy), (x - rx, y))
    pen.curveTo((x - rx, y + bcpy), (x - bcpx, y + ry), (x, y + ry))
    pen.closePath()

def element(pen, x, y, w, h, ratio=BEZIER_ARC_CIRCLE):
    '''
    Draw an element with a pen object.

    '''
    rx = w * 0.5
    ry = h * 0.5
    bcpx = ratio * rx
    bcpy = ratio * ry
    x += rx
    y += ry
    pen.moveTo((x, y + ry))
    pen.curveTo((x + bcpx, y + ry), (x + rx, y + bcpy), (x + rx, y))
    pen.curveTo((x + rx, y - bcpy), (x + bcpx, y - ry), (x, y - ry))
    pen.curveTo((x - bcpx, y - ry), (x - rx, y - bcpy), (x - rx, y))
    pen.curveTo((x - rx, y + bcpy), (x - bcpx, y + ry), (x, y + ry))
    pen.closePath()

#---------------
# drawing tools
#---------------

def drawRectInGlyph(glyph, x, y, w, h):
    '''
    Draw a rectangle in a glyph.

    Args:
        glyph (RGlyph): A glyph object.
        x (int or float): Horizontal position.
        y (int or float): Vertical position.
        w (int or float): The width of the rectangle.
        h (int or float): The height of the rectangle.

    .. code-block:: python

        g = CurrentGlyph()
        drawRectInGlyph(g, 50, 100, 120, 120)

    '''
    print(x, y, w, h)
    pen = glyph.getPen()
    rect(pen, x, y, w, h)

def drawOvalInGlyph(glyph, x, y, w, h):
    '''
    Draw an oval in a glyph.

    Args:
        glyph (RGlyph): A glyph object.
        x (int or float): Horizontal position.
        y (int or float): Vertical position.
        w (int or float): The width of the rectangle.
        h (int or float): The height of the rectangle.

    .. code-block:: python

        g = CurrentGlyph()
        drawOvalInGlyph(g, 50, 100, 120, 120)

    '''
    pen = glyph.getPen()
    oval(pen, x, y, w, h)

def drawElementInGlyph(glyph, x, y, w, h, ratio=BEZIER_ARC_CIRCLE):
    '''
    Draw an element inside a glyph.

    Args:
        glyph (RGlyph): A glyph object.
        x (int or float): Horizontal position.
        y (int or float): Vertical position.
        w (int or float): The width of the rectangle.
        h (int or float): The height of the rectangle.
        ratio (float): The ratio of the handle lengths in relation to width or height.

    .. code-block:: python

        g = CurrentGlyph()
        drawElementInGlyph(g, 50, 100, 120, 120, ratio=0.75)

    '''
    pen = glyph.getPen()
    element(pen, x, y, w, h, ratio)

def addGlyphDrawingTools(RGlyph):
    '''
    Adds drawing methods to RGlyph objects.

    Args:
        RGlyph (RGlyph): The environment’s RGlyph object.

    Call ``addGlyphDrawingTools`` once to add drawing methods to the ``RGlyph`` object::

        from mojo.roboFont import RGlyph
        addGlyphDrawingTools(RGlyph)

    After that it becomes possible to draw shapes in a glyph directly::

        g = CurrentGlyph()
        g.rect(0, 0, 80, 80)
        g.oval(80, 80, 90, 90)
        g.element(170, 170, 100, 100, ratio=0.85)

    '''
    RGlyph.rect    = drawRectInGlyph
    RGlyph.oval    = drawOvalInGlyph
    RGlyph.element = drawElementInGlyph

#---------
# testing
#---------

if __name__ == '__main__':

    from mojo.roboFont import RGlyph

    addGlyphDrawingTools(RGlyph)

    g = CurrentGlyph()
    g.clear()
    g.rect(0, 0, 100, 100)
    g.oval(100, 100, 100, 100)
    g.element(200, 200, 100, 100, ratio=0.85)
