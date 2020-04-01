---
layout: default
title: Build glyphs
---

Create new glyphs in the selected fonts.

fonts
-----

Select on which fonts to build the glyphs.

<div class='row'>

<div class='col' markdown='1'>
![]({{ site.url }}/images/batch/BatchBuild_0.png)
</div>

<div class='col' markdown='1'>
target fonts
: a list of open and/or closed fonts for selection

add all open fonts
: add all open fonts to the list

select all
: select all fonts in the list

add fonts folder
: add a folder with UFOs to the list

clear font lists
: empties the list of fonts
</div>

</div>

new
---

Create new empty glyphs in the selected fonts.

<div class='row'>

<div class='col' markdown='1'>
![]({{ site.url }}/images/batch/BatchBuild_1.png)
</div>

<div class='col' markdown='1'>
glyph names
: as a space-separated list

batch make glyphs
: build new glyphs in the selected fonts

preflight
: simulate the action before applying it
</div>

</div>

constructions
-------------

Create new glyphs from glyph construction rules.

<div class='row'>

<div class='col' markdown='1'>
![]({{ site.url }}/images/batch/BatchBuild_2.png)
</div>

<div class='col' markdown='1'>
import constructions
: import constructions from a `.glyphConstruction` file

construction rules
: glyph definitions in glyph construction syntax for creating new glyphs

export constructions
: export constructions to a `.glyphConstruction` file

select glyphs
: select the new glyphs after they are created

mark glyphs
: ^
  apply a mark color to the new glyphs
  click on the button to choose a color

batch build glyphs
: build the glyphs in the selected fonts

preflight
: simulate the action before applying it
</div>

</div>

- - -

> - add default width to *new* section
{: .todo }
