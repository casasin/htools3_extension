# menuTitle : export layer

import os, shutil
from mojo.UI import GetFolder

f = CurrentFont()

layerName = '151'
overwrite = True
openLayerFont = True

if f is not None:

    # get layer
    assert layerName in f.layerOrder
    layer = f.getLayer(layerName)

    # insert layer in new font
    f2 = NewFont(showInterface=False)
    newLayer = f2.insertLayer(layer, name=layerName)

    # make layer the default and only layer
    f2.defaultLayer = newLayer
    if 'foreground' in f2.layerOrder:
        f2.removeLayer('foreground')
    
    # copy some font infos from source font
    attrs = ['familyName', 'xHeight', 'capHeight', 'descender', 'ascender', 'unitsPerEm']
    for attr in attrs:
        value = getattr(f.info, attr)
        setattr(f2.info, attr, value)
    f2.info.styleName = layerName
    f2.glyphOrder = f.glyphOrder

    # get layer UFO path
    if f.path is None:
        folder = GetFolder(message='Please choose a folder to save the UFO.', title='export layer')
    else:
        folder = os.path.dirname(f.path)
    fontPath = os.path.join(folder, f'{layerName}.ufo')

    # remove existing UFO
    if os.path.exists(fontPath):
        if overwrite:
            shutil.rmtree(fontPath)
        else:
            print('a file with this name already exists')

    # save layer to UFO
    if not os.path.exists(fontPath):
        f2.save(fontPath)

# open exported layer font
if openLayerFont:
    OpenFont(fontPath)
