---
layout: default
title: Copy data
---

Copy data from one source font to all selected target fonts.

### fonts

Select source and target fonts.

<div class='row'>

<div class='col' markdown='1'>
![]({{ site.url }}/images/batch/BatchCopy_0.png)
</div>

<div class='col' markdown='1'>
source font
: select the source font from which to copy data

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

### font info

Copy the selected font info attributes.

<div class='row'>

<div class='col' markdown='1'>
![]({{ site.url }}/images/batch/BatchCopy_1.png)
</div>

<div class='col' markdown='1'>
select all
: select all attributes in all groups

attributes
: select/deselect font info attributes to copy

copy font info
: copy the selected font info attributes

preflight
: simulate the action before applying it
</div>

</div>

### glyphs

<div class='row'>

<div class='col' markdown='1'>
![]({{ site.url }}/images/batch/BatchCopy_2.png)
</div>

<div class='col' markdown='1'>
Use the *glyphs* section to select glyphs to copy from the source font to the target fonts.

Use the radio button to choose one of the available glyph selection methods.

Use the list to select which types of glyph data to copy.

Select *remove source glyphs* to delete the source glyphs after copying.

Select *clear target glyphs* to delete the target glyph’s contours before copying.

Select *select target glyphs* to select the glyphs after copying.

Select *mark target glyphs* to apply a mark color to the copied glyphs. Click on the button to open the Color Well and choose a color.

Select *preflight* to simulate the action before applying it.
</div>

</div>

### kerning

![]({{ site.url }}/images/batch/BatchCopy_3.png)

Click on the *copy kerning* button to copy kerning data from the source font to the target fonts.

Select *clear target kerning* to delete the target font’s kerning before copying.

Select *preflight* to simulate the action before applying it.

### groups

Click on the *copy groups* button to copy groups from the source font to the target fonts.

Select *clear target groups* to delete the target font’s groups before copying.

Select the types of group to copy: plain groups and/or kerning groups.

Select *preflight* to simulate the action before applying it.

### features

Click on the *copy features* button to copy OpenType features from the source font to the target fonts.
