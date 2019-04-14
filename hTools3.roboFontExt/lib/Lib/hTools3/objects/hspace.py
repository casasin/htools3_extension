import os
from itertools import product
from mojo.roboFont import RFont, NewFont
from hTools3.objects.hproject import hProject

# from hTools2_plus.objects.hfont import hFont
# from hTools2.modules.anchors import transfer_anchors, move_anchors
# from hTools2.modules.fileutils import get_names_from_path
# from hTools2.modules.fontinfo import clear_opentype_os2, clear_opentype_hhea, clear_opentype_vhea
# from hTools2.modules.fontutils import rename_glyphs_from_list, get_full_name, scale_glyphs, parse_glyphs_groups
# from hTools2.modules.ftp import connect_to_server, upload_file
# from hTools2.modules.glyphutils import *
# from hTools2.modules.vmetrics import set_vmetrics

class hSpace:

    project = None

    parameters = {}

    fonts = {}

    def __init__(self, folder):
        self.project = hProject(folder)

    def __repr__(self):
        return '<hSpace3 %s>' % self.project.name

    @property
    def parameters(self):
        return product(*[self.project.lib['parameters'][p] for p in self.project.lib['parametersOrder']])

    @property
    def fontNames(self):
        return ['-'.join([str(p) for p in params]) for params in self.parameters]

    def setParameters(self, parameters):
        pass

    def ufos(self):
        pass

    def getGlyphNames(self, gstring):
        pass

    def createFonts(self):
        pass

    def createGlyphs(self, gstring=None, verbose=False):
        pass

    def buildAccents(self, gstring=None, ignore=[]):
        pass

    def clearKerning(self):
        pass

    def clearUnicodes(self):
        pass

    def clearInfo(self):
        pass

    def clearGroups(self):
        pass

    def clearFeatures(self):
        pass

    def clearAnchors(self):
        pass

    def transferGlyphs(self, var, gstring, verbose=False):
        pass

    def shiftX(self, dest_width, gstring, pos, delta, side, verbose=True):
        pass

    def shiftY(self, destHeight, gstring, transformations, verbose=True):
        pass


if __name__ == '__main__':

    folder = '/Volumes/gf_bkp_3/_fonts/gridfonts/Elementar'
    S = hSpace(folder)
    # print(list(S.parameters))
    # print(list(S.fontNames))

