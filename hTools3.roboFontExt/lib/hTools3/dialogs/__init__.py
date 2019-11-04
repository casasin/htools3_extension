# coding: utf-8

import os
from AppKit import NSApp
from vanilla import FloatingWindow, HUDFloatingWindow, Window
from mojo.roboFont import CurrentGlyph, CurrentFont, AllFonts
from mojo.extensions import getExtensionDefault, getExtensionDefaultColor, setExtensionDefault, setExtensionDefaultColor
from hTools3.modules.fontutils import getGlyphs
from hTools3.modules.messages import *
from hTools3.modules.color import rgbToNSColor, nsColorToRGB

class hDialogBase(object):

    '''
    A base object with dimensions and settings for all hTools3 dialogs.

    '''

    padding      = 10
    sizeStyle    = 'small'
    textHeight   = 20
    textInput    = 18
    progressBar  = 6
    buttonHeight = 25
    buttonNudge  = 18
    buttonSquare = 35
    width        = 123 # buttonNudge * 6 - 5 + padding * 2

    #: The type of the window. 0=FloatingWindow, 1=HUDFloatingWindow, 2=Window
    windowType   = 0
    windowTypes  = [FloatingWindow, HUDFloatingWindow, Window]

    @property
    def spinnerHeight(self):
        return self.buttonNudge * 2 + self.padding

    @property
    def arrowsHeight(self):
        return self.width

class hDialog(hDialogBase):

    '''
    A base object which provides generic functionality for all hTools3 dialogs.

    '''

    key      = 'com.hipertipo.hTools3.dialogs'
    prefsKey = 'com.hipertipo.hTools3.preferences'
    prefsDefaults = {
        'previewFillColor'    : (0, 1, 0, 0.35),
        'previewStrokeColor'  : (0, 1, 0),
        'previewStrokeWidth'  : 2,
        'previewOriginRadius' : 10,
        'verbose'             : True,
    }

    # settings = {}
    # settingsSave = False
    # verbose  = True
    # readOnly = False

    # -------------
    # dynamic attrs
    # -------------

    # preview fill color

    @property
    def previewFillColorKey(self):
        return '%s.previewFillColor' % self.prefsKey

    @property
    def previewFillColor(self):
        color = getExtensionDefaultColor(self.previewFillColorKey, fallback=self.prefsDefaults['previewFillColor'])
        if type(color) is not tuple:
            color = nsColorToRGB(color)
        return color

    @previewFillColor.setter
    def previewFillColor(self, color):
        if type(color) is tuple:
            color = rgbsToNSColor(color)
        setExtensionDefaultColor(self.previewFillColorKey, color)

    # preview stroke color

    @property
    def previewStrokeColorKey(self):
        return '%s.previewStrokeColor' % self.prefsKey

    @property
    def previewStrokeColor(self):
        color = getExtensionDefaultColor(self.previewStrokeColorKey, fallback=self.prefsDefaults['previewStrokeColor'])
        if type(color) is not tuple:
            color = nsColorToRGB(color)
        return color

    @previewStrokeColor.setter
    def previewStrokeColor(self, color):
        if type(color) is tuple:
            color = rgbToNSColor(color)
        setExtensionDefaultColor(self.previewStrokeColorKey, color)

    # preview stroke width

    @property
    def previewStrokeWidthKey(self):
        return '%s.previewStrokeWidth' % self.prefsKey

    @property
    def previewStrokeWidth(self):
        return getExtensionDefault(self.previewStrokeWidthKey, fallback=self.prefsDefaults['previewStrokeWidth'])

    @previewStrokeWidth.setter
    def previewStrokeWidth(self, value):
        setExtensionDefault(self.previewStrokeWidthKey, value)

    # preview origin radius

    @property
    def previewOriginRadiusKey(self):
        return '%s.previewOriginRadius' % self.prefsKey

    @property
    def previewOriginRadius(self):
        return getExtensionDefault(self.previewOriginRadiusKey, fallback=self.prefsDefaults['previewOriginRadius'])

    @previewOriginRadius.setter
    def previewOriginRadius(self, value):
        setExtensionDefault(self.previewOriginRadiusKey, value)

    # verbose mode

    @property
    def verboseKey(self):
        return '%s.verbose' % self.prefsKey

    @property
    def verbose(self):
        return getExtensionDefault(self.verboseKey, fallback=self.prefsDefaults['verbose'])

    @verbose.setter
    def verbose(self, value):
        setExtensionDefault(self.verboseKey, value)

    @property
    def window(self):
        '''
        Return the vanilla window object for the dialog.

        '''
        return self.windowTypes[self.windowType]

    # -------
    # methods
    # -------

    def loadSettings(self):
        print('load_settings')
        # TODO:
        # read extension settings for tool
        # save it as a hSettings object
        # self.settings = hSettings(settingsDict)
        pass

    def saveSettings(self):
        # TODO:
        print('save_settings')
        pass

    def getCurrentFont(self):
        '''
        Get the current font. Print a message if there is no current font.

        Returns:
            A font object (RFont).

        '''
        font = CurrentFont()
        if not font:
            print(noFontOpen)
        return font

    def getCurrentGlyph(self):
        '''
        Get the current glyph. Print a message if there is no current glyph.

        Returns:
            A glyph object (RGlyph).

        '''
        glyph = CurrentGlyph()
        if not glyph:
            print(noGlyphOpen)
        return glyph

    def getLayerNames(self):
        '''
        Get the current layer selection in the 'layers' panel.

        Returns:
            A list of layer names.

        '''
        app = NSApp()
        layers = []
        selection = []
        for window in app.windows():
            if window.title() == 'layers':
                delegate = window.delegate()
                if hasattr(delegate, "vanillaWrapper"):
                    vanillaWrapper = delegate.vanillaWrapper
                    layers.extend(vanillaWrapper.w.list.get())
                    selection.extend(vanillaWrapper.w.list.getSelection())

        return [layer for i, layer in enumerate(layers) if i in selection]

    def getGlyphNames(self):
        '''
        Get the current glyph selection in the current font.

        Returns:
            A list of glyph names.

        '''
        font = self.getCurrentFont()

        if not font:
            return

        glyphNames = getGlyphs(font)

        if not len(glyphNames):
            print(noGlyphSelected)

        return glyphNames

    def getAllFonts(self):
        '''
        Get all open fonts. Print a message if no font is open.

        Returns:
            A list of font objects (RFont).

        '''
        allFonts = AllFonts()

        if not len(allFonts):
            print(noFontOpen)

        return allFonts

    def getFontsFolder(self, folder):
        '''
        Get the paths of all fonts in a folder. Print a message if the folder contains no fonts.

        Returns:
            A list of font objects (RFont).

        '''
        fontPaths = []
        for f in os.listdir(folder):
            if not os.path.splitext(f)[-1] == '.ufo':
                continue
            fontPath = os.path.join(folder, f)
            fontPaths.append(fontPath)

        if not len(fontPaths):
            print(noFontInFolder)

        return fontPaths

# class hSettings:

#     # TODO: implement reading & writing settings

#     plistPath = None

#     def __init__(self, settingsDict={}):
#         for key, value in settingsDict.items():
#             setattr(self, key, value)

#     def read(self, plistPath):
#         # 1. read plist
#         # 2. map values to hSettings attributes
#         pass

#     def write(self, plistPath=None):
#         # 1. make a dict of all attributes/values
#         # 2. save dict to plist
#         pass
