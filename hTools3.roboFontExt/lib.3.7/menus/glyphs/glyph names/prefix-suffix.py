# menuTitle : prefix suffix

from importlib import reload
import hTools3.dialogs.glyphs.namesSuffix
reload(hTools3.dialogs.glyphs.namesSuffix)

from mojo.roboFont import OpenWindow
from hTools3.dialogs.glyphs.namesSuffix import PrefixSuffixGlyphNamesDialog

OpenWindow(PrefixSuffixGlyphNamesDialog)
