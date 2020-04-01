---
layout: default
title: Build glyphs
---

Create new glyphs in the selected fonts.

### fonts

Use the *fonts* section to select on which fonts to build the glyphs.

### new

Use the *new* section to create new empty glyphs in the selected fonts.

<div class='container'>

<div class='screenshot' markdown='1'>
![]({{ site.url }}/images/batch/BatchBuild_1.png)
</div>

<div class='captions' markdown='1'>
glyph names
: as a space-separated list

batch make glyphs
: build new glyphs in the selected fonts

preflight
: simulate the action before applying it
</div>

</div>

### constructions

<div class='container'>

<div class='screenshot' markdown='1'>
![]({{ site.url }}/images/batch/BatchBuild_2.png)
</div>

<div class='captions' markdown='1'>
import constructions
: import constructions from a `.glyphConstruction` file

glyph constructions
: glyph definitions in glyph construction syntax for creating new glyphs

export constructions…
: export the current constructions to a `.glyphConstruction` file

select glyphs
: select the new glyphs after they are created.

mark glyphs
: ^
  apply a mark color to the transformed glyphs.  click on the button to choose a color

batch build glyphs
: build the glyphs in the selected fonts

preflight
: simulate the action before applying it
</div>

</div>

- - -

### to-do

- add default width to *new* section
