
def getMinMaxY(font, r=None):
    yMax_ = []
    yMin_ = []
    for g in font:
        if g.bounds is not None:
            xMin, yMin, xMax, yMax = g.bounds
            yMax_.append(yMax)
            yMin_.append(yMin)
    yMax = max(yMax_)
    yMin = min(yMin_)
    if r is not None:
        yMin = int((yMin // r) * r)
        yMax = int((yMax // r) * r)
    return yMin, yMax

def setVMetrics(font, xheight, capheight, ascender, descender, emsquare, gridsize=1):
    font.info.xHeight = xheight * gridsize
    font.info.capHeight = capheight * gridsize
    font.info.descender = -abs(descender * gridsize)
    font.info.ascender = ascender * gridsize
    font.info.unitsPerEm = emsquare * gridsize

def autoSetVMetrics(font, ascender, descender, ymax, ymin):
    '''
    Automatically set vertical metrics info attributes from ascender, descender and min/max Y values.

    '''
    hheaAscender     = ymax
    hheaDescender    = ymin
    hheaLinegap      = 0
    OS2WinAscent     = ymax
    OS2WinDescent    = abs(ymin)
    OS2TypoAscender  = ascender
    OS2TypoDescender = descender
    OS2TypoLinegap   = (OS2WinAscent + abs(OS2WinDescent)) - (OS2TypoAscender + abs(OS2TypoDescender))

    font.info.ascender                 = ascender
    font.info.descender                = -descender
    font.info.unitsPerEm               = ascender + descender
    font.info.openTypeHheaAscender     = hheaAscender
    font.info.openTypeHheaDescender    = hheaDescender
    font.info.openTypeHheaLineGap      = hheaLinegap
    font.info.openTypeOS2TypoAscender  = OS2TypoAscender
    font.info.openTypeOS2TypoDescender = -OS2TypoDescender
    font.info.openTypeOS2TypoLineGap   = OS2TypoLinegap
    font.info.openTypeOS2WinAscent     = OS2WinAscent
    font.info.openTypeOS2WinDescent    = OS2WinDescent

    roundVMetrics(font)

def roundVMetrics(font):
    vmetricsAttributes = [
        "ascender",
        "descender",
        "unitsPerEm",
        "openTypeHheaAscender",
        "openTypeHheaDescender",
        "openTypeHheaLineGap",
        "openTypeOS2TypoAscender",
        "openTypeOS2TypoDescender",
        "openTypeOS2TypoLineGap",
        "openTypeOS2WinAscent",
        "openTypeOS2WinDescent",
    ]
    for attribute in vmetricsAttributes:
        value = getattr(font.info, attribute)
        setattr(font.info, attribute, int(value))

def setVMetricsLineHeight(font, ratio=0.75, linespace=None):

    if linespace is None:
        lineAuto = True
    else:
        lineAuto = False

    unitsPerEm = font.info.unitsPerEm
    ascender   = unitsPerEm * ratio
    descender  = unitsPerEm * (1.0 - ratio)

    if lineAuto:
        yMin, yMax = getMinMaxY(font, r=5)
    else:
        yMin = -(descender * linespace)
        yMax = ascender * linespace

    autoSetVMetrics(font, int(ascender), int(descender), int(yMax), int(yMin))
