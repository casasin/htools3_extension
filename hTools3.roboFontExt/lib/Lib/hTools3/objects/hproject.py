import os
import shutil
# import json
import plistlib
from hTools3.modules.encoding import importEncoding, importGroupsFromEncoding

class hProject(object):

    def __init__(self, folder):
        self.folder = folder

    def __repr__(self):
        return '<hProject3 %s>' % self.name

    # -------------
    # dynamic attrs
    # -------------

    @property
    def name(self):
        return os.path.split(self.folder)[-1].replace('_', ' ')

    # subfolders

    @property
    def ufosFolder(self):
        return os.path.join(self.folder, '_ufos')

    @property
    def instancesFolder(self):
        return os.path.join(self.ufosFolder, 'instances')

    @property
    def otfsFolder(self):
        return os.path.join(self.folder, '_otfs')

    @property
    def ttfsFolder(self):
        return os.path.join(self.folder, '_ttfs')

    @property
    def libsFolder(self):
        return os.path.join(self.folder, '_libs')

    # file lists

    @property
    def masters(self):
        if not os.path.exists(self.ufosFolder):
            return []
        else:
            return [os.path.join(self.ufosFolder, f) for f in os.listdir(self.ufosFolder) if os.path.splitext(f)[1] == '.ufo']

    @property
    def instances(self):
        if not os.path.exists(self.instancesFolder):
            return []
        else:
            return [os.path.join(self.instancesFolder, f) for f in os.listdir(self.instancesFolder) if os.path.splitext(f)[1] == '.ufo']

    @property
    def otfs(self):
        if not os.path.exists(self.otfsFolder):
            return []
        else:
            return [os.path.join(self.otfsFolder, f) for f in os.listdir(self.otfsFolder) if os.path.splitext(f)[1] == '.otf']

    @property
    def ufos(self):
        return self.masters + self.instances

    @property
    def fonts(self):
        D = {}
        for ufo in self.ufos:
            ufoName = os.path.splitext(os.path.split(ufo)[-1])[0]
            D[ufoName] = ufo
        return D

    # data paths

    @property
    def libPath(self):
        return os.path.join(self.libsFolder, 'project.plist')

    @property
    def encodingPath(self):
        return os.path.join(self.libsFolder, 'encoding.enc')

    @property
    def featuresPath(self):
        return os.path.join(self.libsFolder, 'features.fea')

    @property
    def infosPath(self):
        return os.path.join(self.libsFolder, 'fontinfo.plist')

    @property
    def accentsPath(self):
        return os.path.join(self.libsFolder, 'accents.glyphConstruction')

    @property
    def designspacePath(self):
        return os.path.join(self.ufosFolder, 'interpolation.designspace')

    # data

    @property
    def lib(self):
        with open(self.libPath, 'rb') as f:
            L = plistlib.load(f)
        return L

    @lib.setter
    def lib(self, lib):
        with open(self.libPath, 'wb') as f:
            plistlib.dump(lib, f)

    @property
    def glyphset(self):
        return importEncoding(self.encodingPath)

    @property
    def groups(self):
        return importGroupsFromEncoding(self.encodingPath)

    @property
    def accents(self):
        # if os.path.exists(self.accents_path):
        #     return readPlist(self.accents_path)
        pass

    @property
    def vmetrics(self):

        # if os.path.exists(self.vmetrics_path):
        #     return readPlist(self.vmetrics_path)

        # print('importing font info from file…')
        # # read font info from json
        # with open(jsonPath, 'r', encoding='utf-8') as inputFile:
        #     self.fontInfoData = json.load(inputFile)
        # # load font info dict into UI
        # self.loadFontInfoDict(self.fontInfoData)

        pass

    # -------
    # methods
    # -------

    # clear files

    def clearInstances(self):
        pass

    def clearVariableFont(self):
        pass

    def clearOTFs(self):
        pass

    def clearTTFs(self):
        pass

    def clearWOFFs(self):
        pass

    # font generation

    def generateInstances(self, kerning=False, clear=True, neutral=None, add_infos=False):
        pass

    def generateVariableFont(self):
        pass

    def generateOTFs(self):
        pass

    def generateTTFs(self):
        pass

    def generateWOFFs(self):
        pass

    def generateCSS(self):
        pass

    # proofing

    def makeTextProof(self):
        pass

    def makeGlyphsGridProof(self):
        pass

    def makeHTMLProof(self):
        pass

    # shipping

    def buildPackage(self):
        pass

# -------
# testing
# -------

if __name__ == '__main__':

    folder = '/_fonts/Jornalistica_Roman'

    p = hProject(folder)

    print(p)
    print(p.name)

    print(p.libsFolder)
    print(p.ufosFolder)
    print(p.instancesFolder)
    print(p.otfsFolder)

    print(p.masters)
    print(p.instances)
    print(p.otfs)

    print(p.libPath)
    print(p.encodingPath)
    print(p.featuresPath)
    print(p.infosPath)
    print(p.accentsPath)
    print(p.designspacePath)
    print(p.vmetricsPath)

    print(p.groups)
