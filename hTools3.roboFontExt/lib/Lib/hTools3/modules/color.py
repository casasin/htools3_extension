# coding: utf-8

'''
Tools to convert between different color models.

'''

from AppKit import NSColor

def rgbToNSColor(rgbColor):
    '''
    Convert RGB color tuple to NSColor object.

    Args:
        rgbColor (tuple): RGB color as a tuple of 1, 2, 3 or 4 values (floats between 0 and 1).

    Returns:
        A NSColor object.

    >>> rgbColor = 1, 0, 0
    >>> nsColor = rgbToNSColor(rgbColor)
    >>> print(nsColor)
    NSCalibratedRGBColorSpace 1 0 0 1

    '''
    if rgbColor is None:
        return
    elif len(rgbColor) == 1:
        r = g = b = rgbColor[0]
        a = 1.0
    elif len(rgbColor) == 2:
        grey, a = rgbColor
        r = g = b = grey
    elif len(rgbColor) == 3:
        r, g, b = rgbColor
        a = 1.0
    elif len(rgbColor) == 4:
        r, g, b, a = rgbColor
    else:
        return
    nsColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(r, g, b, a)
    return nsColor

def nsColorToRGB(nsColor):
    '''
    Convert from NSColor object to RGBA color tuple.

    Args:
        nsColor (NSColor): A color object.

    Returns:
        A tuple of RGBA values.

    >>> nsColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(0, .5, 1, .8)
    >>> rgbColor = nsColorToRGB(nsColor)
    >>> print(rgbColor)
    (0.0, 0.5, 1.0, 0.8)

    '''
    r = nsColor.redComponent()
    g = nsColor.greenComponent()
    b = nsColor.blueComponent()
    a = nsColor.alphaComponent()
    return r, g, b, a

nsColorToRGBa = nsColorToRGB

def hexToRGB(hexColor):
    '''
    Convert hexadecimal color to RGB color tuple.

    Args:
        hexColor (str): A hexadecimal color.

    Returns:
        A tuple of RGB values.

    >>> hexColor = 'FF0099'
    >>> rgbColor = hexToRGB(hexColor)
    >>> print(rgbColor)
    (1.0, 0.0, 0.6)

    '''
    hexColor = hexColor.lstrip('#')
    lv = len(hexColor)
    rgb = tuple()
    for i in range(0, lv, lv//3):
        rgb += (int(hexColor[i:i+lv//3], 16) / 255.0,)
    return rgb

def RGBToHex(rgbColor):
    '''
    Convert RGB color tuple to hexadecimal color.

    Args:
        rgbColor (tuple): RGB color as a tuple of 3 values.

    Returns:
        A hexadecimal color.

    >>> rgbColor = 1.0, 0.2, 0.0
    >>> hexColor = RGBToHex(rgbColor)
    >>> print(hexColor)
    ff3300

    '''
    r, g, b = rgbColor
    r, g, b = int(r*255), int(g*255), int(b*255)
    return '%02x%02x%02x' % (r, g, b)

