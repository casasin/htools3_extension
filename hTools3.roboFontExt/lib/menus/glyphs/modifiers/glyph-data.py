# menuTitle : glyph data

from importlib import reload
import hTools3.dialogs.glyphs.modifiersGlyphData
reload(hTools3.dialogs.glyphs.modifiersGlyphData)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.glyphs.modifiersGlyphData import SelectGlyphDataDialog

OpenWindow(SelectGlyphDataDialog)
