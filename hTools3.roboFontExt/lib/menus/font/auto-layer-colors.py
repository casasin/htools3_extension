# menuTitle : auto layer colors

from colorsys import hsv_to_rgb

def autoLayerColors(font):
    hueStep = 1.0 / len(f.layerOrder)
    for i, layerName in enumerate(f.layerOrder):
        c = hsv_to_rgb(i * hueStep, 1.0, 0.8)
        c += (1.0,)
        layer = f.getLayer(layerName)
        layer.color = c
    font.changed()

f = CurrentFont()

if f:
    autoLayerColors(f)
