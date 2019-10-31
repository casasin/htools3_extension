hTools3
=======

hTools3 is a modular toolkit for RoboFont 3.


Overview
--------

All tools are available from a single *hTools3* entry in the main menu.

The submenus of the *hTools3* menu correspond to different categories. Each category of tool is developed to a certain scope and corresponding action patterns. 

#### *glyphs*

Tools in this category apply actions to the selected glyphs in the [Font Overview] and/or to the current glyph in the [Glyph Editor]. Actions are applied to the default layer (or the current layer in the Glyph Editor) by default. Individual layers and data types can be referenced using separate *layers* and *dlyph data* modifier panels.

Tools in this category are the most numerous ones in hTools3. To make options more accessible, the *glyphs* menu is further divided into submenus according to which type of data they change or which type of action they perform. Examples: anchors, contours, components, guidelines, interpolation, layers, mark color,  etc.

- Tools in this category are included in the [hTools3 core] module.

[Font Overview]: #
[Glyph Editor]: #
[hTools3 core]: #

#### *font*

Tools in this category apply actions to font-level data in the current font. Examples of font-level data: font info, kerning, groups, font guidelines, etc.

- Tools in this category are included in the [hTools3 core] module.

#### batch

Tools in this category apply actions to a list of closed and/or open fonts. Different batch tools use different action patterns, for example some tools transform data in fonts, some tools copy data between fonts, some tools copy data from external files into fonts, etc.

Batch tools are very fast and ideal for large families and large scale ‘industrial’ font production projects.

- Tools in this category are available separately from the [hTools3 batch] module.

#### glyph

visualizations in the glyph editor (current glyph)

- available separately from the `hTools3_glyph` module

#### proofing

making different kinds of proofs for selected font(s)

- available separately from the `hTools3_proofing` module

#### effects

available separately from individual modules:

- `hTools3_underliner`
- `hTools3_rasterizer`
- `hTools3_strokesetter`
- `hTools3_stripes`
- `hTools3_blur`


## Pricing scheme

Commercial extensions distributed via the Extension Store and Mechanic 2:

| extension | single license price |
|-|-|
| [hTools3 core] | €150 |
| [hTools3 batch tools] | €150 |
| [hTools3 glyph tools] | €50 |
| [hTools3 proofing tools] | €50 |

Other hTools3-based extensions available directly from Hipertipo on request

| [rasterizer] |
| [underliner] |
| [strokesetter] |


[hTools3 glyph tools]: #
[hTools3 batch tools]: #
[hTools3 proofing tools]: #
[rasterizer]: #
[underliner]: #
[strokesetter]: #
