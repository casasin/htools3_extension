# coding: utf-8

import os
from fontTools import subset

def subsetOTF(srcFontPath, dstFontPath, glyphNames, obfuscateNames=False, removeFeatures=False, removeKerning=False, removeHinting=False, verbose=True):
    '''
    Subset an OpenType font using the fontTools subsetter.

    Args:
        srcFontPath (str): The path to the source OpenType font.
        dstFontPath (str): The path to the target subsetted OpenType font.
        glyphNames (list): A list of glyph names to be included in the subsetted font.
        obfuscateNames (bool): Obfuscate font names.
        removeFeatures (bool): Remove all OpenType features.
        removeKerning (bool): Remove all kerning.
        removeHinting (bool): Remove hinting data.

    Returns:
        A boolean indicating if the subsetted font was generated.

    .. code-block:: python

        from hTools3.modules.webfonts import subsetOTF
        srcFont = '/path/to/myFont.otf'
        dstFont = srcFont.replace('.otf', '_subset.otf')
        glyphNames = 'space exclam quotedbl numbersign dollar percent ampersand quotesingle parenleft parenright asterisk plus comma hyphen period slash zero one two three four five six seven eight nine colon semicolon less equal greater question at A B C D E F G H I J K L M N O P Q R S T U V W X Y Z bracketleft backslash bracketright asciicircum underscore grave a b c d e f g h i j k l m n o p q r s t u v w x y z braceleft bar braceright asciitilde'.split()
        subsetOTF(srcFont, dstFont, glyphNames, obfuscateNames=False, removeFeatures=False, removeKerning=False, removeHinting=False, verbose=True)

    '''
    # input & output fonts
    command  = [srcFontPath]
    command += ["--output-file=%s" % dstFontPath]

    # glyph set
    command += ["--glyphs=%s" % ','.join(glyphNames)]
    command += ["--ignore-missing-glyphs"]

    # name options
    command += ["--name-IDs=*"]
    command += ["--name-languages=0,1033"]
    command += ["--name-legacy"]
    if obfuscateNames:
        command += ["--obfuscate-names"]

    # features & kerning
    if removeKerning and removeFeatures:
        # kerning  NO  / features NO
        command += ["--layout-features=''"]
        command += ["--no-legacy-kern"]
    elif not removeKerning and removeFeatures:
        # kerning  YES / features NO
        command += ["--layout-features='kern'"]
        command += ["--legacy-kern"]
    elif removeKerning and not removeFeatures:
        # kerning  NO  / features YES
        command += ["--layout-features-='kern'"]
        command += ["--no-legacy-kern"]
    else:
        # kerning  YES / features YES
        command += ["--legacy-kern"]

    # hinting
    if removeHinting:
        command += ["--no-hinting"]
        command += ["--desubroutinize"]
        command += ["--hinting-tables=''"]

    if verbose:
        command += ["--verbose"]

    # run subset command
    subset.main(command)

    # done!
    return os.path.exists(dstFontPath)
