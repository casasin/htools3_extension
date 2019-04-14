======
glyphs
======

Glyphs tools apply one or more actions to the selected glyphs in the current font. Glyph selection includes glyphs selected in the Font Overview, and the glyph in the current Glyph Window (if one is open).

Glyphs tools form the largest and most diverse group of tools in hTools3. The dialogs in this group are organized in submenus based on the type of data they modify (for ex: layers, metrics, glyph names, transformations, etc).

Some tools transform glyphs in the current font only; others copy data between fonts. Tools which transform visual glyph data may show a preview of the current settings in the background of the Glyph View.

Glyphs tools are built using translucent floating windows, and share the same width and interface patterns. Numerical values can be modified interactively using sliders and spinners, with a live preview of the result.

.. toctree::
   :maxdepth: 1

   base
   anchorsCreate
   namesPrint
   namesSuffix
   gridfit
   boolean
   outline
   underline
   blur
   interpolationMasters
   interpolationCheck
   interpolationCondense
   interpolationInFont
   layersImport
   layersLock
   layersMask
   marginsCopy
   marginsSet
   widthCopy
   widthSet
   scale
   move
   rotate
   skew
   shiftPoints
   actions
   balanceHandles
   markSelect
   markTypes
   modifiersGlyphData
   modifiersLayers
