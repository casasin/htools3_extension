---
layout: default
---

<!--
Batch tools apply one or more actions to several fonts at once. Both open and closed fonts are supported. Some Batch tools can import/export data to text files.

All Batch tools are built using the Accordion View, with controls and settings grouped in collapsible sections (panes). The first pane of all Batch tools is the font selection pane. Other panes offer additional action settings and buttons to apply actions.

Batch tools provide no visual feedback for changes in the fonts, so it’s important to backup your data and make tests before applying a transformation to many fonts. All Batch tools include a preflight function to test the current settings without actually applying the changes.
-->


actions
-------

Apply glyph-level actions to selected fonts.

### fonts

Use the *fonts* section to select on which fonts the actions should be applied.

### glyphs

![](/images/batch/BatchActions_1.png)

Use the *glyphs* section to select on which glyphs the actions should be applied.

Use the radio button to choose one of the available glyph selection methods.

Select <em>mark glyphs</em> to apply a mark color to the transformed glyphs. Click on the button to open the Color Well and choose a color.

### actions

![](/images/batch/BatchActions_2.png)

Select actions to apply from the list.

Drag the list items to change the order in which the actions are applied.

The option between PostScript and TrueType applies only to *correct contour direction*.

Use the *apply selected actions* button to apply the selected actions.

Select *preflight* to simulate the actions before applying them.


clear data
----------

Clear different kinds of font data in the selected fonts.

### fonts

Use the *fonts* section to select on which fonts to build glyphs.

### font info

![](/images/batch/BatchClear_1.png)

Select font info attributes to clear.

Use the *select all* checkbox to select all attributes.

Select/deselect a group of attributes at once by clicking in the attribute categories.

Click on the *clear font info* button to clear the selected font info attributes.

Select *preflight* to simulate the action before applying it.

### font data

![](/images/batch/BatchClear_2.png)

Select different types of font data to clear.

Use the *select all* checkbox to select all data types.

Click on the *clear font data* button to clear the selected data types.

Select *preflight* to simulate the action before applying it.


build glyphs
------------

Create new glyphs in the selected fonts.

### fonts

Use the *fonts* section to select on which fonts to build glyphs.

### new

![](/images/batch/BatchBuild_1.png)

A space-separated list of glyph names to build.

Click on the *batch make glyphs* button to build the glyphs.

Select *preflight* to simulate the action before applying it.

### constructions

![](/images/batch/BatchBuild_2.png)

Use the *import constructions…* button to import constructions from a `.glyphConstruction` file.

Use the text area to write glyph construction rules for new glyphs.

Use the `export constructions…` button to export the current constructions to a `.glyphConstruction` file.

Select `select glyphs` to select the new glyphs after they are created.

Select `mark glyphs` to apply a mark color to the transformed glyphs. Click on the button to open the Color Well and choose a color.

Click on the `batch build glyphs` button to build the glyphs.

Select `preflight` to simulate the action before applying it.


copy data
---------

Copy data from one source font to all selected target fonts.

### fonts

Use the *fonts* section to select source and target fonts.

### font info

![](/images/batch/BatchCopy_1.png)

Select font info attributes to copy.

Use the *select all* checkbox to select all attributes.

Select/deselect a group of attributes at once by clicking in the attribute categories.

Click on the *clear font info* button to clear the selected font info attributes.

Select *preflight* to simulate the action before applying it.

### glyphs

![](/images/batch/BatchCopy_2.png)

Use the *glyphs* section to select glyphs to copy from the source font to the target fonts.

Use the radio button to choose one of the available glyph selection methods.

Use the list to select which types of glyph data to copy.

Select *remove source glyphs* to delete the source glyphs after copying.

Select *clear target glyphs* to delete the target glyph’s contours before copying.

Select *select target glyphs* to select the glyphs after copying.

Select *mark target glyphs* to apply a mark color to the copied glyphs. Click on the button to open the Color Well and choose a color.

Select *preflight* to simulate the action before applying it.

### kerning

![](/images/batch/BatchCopy_3.png)

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


set data
--------

Set data in all selected fonts.

### fonts

Use the <em>fonts</em> section to select on which fonts to set data.

### font info

![](/images/batch/BatchSet_1.png)

Use the *font info* section to define which font attributes to set.

Use the *Import info from UFO* button to import font info values from a `.ufo` font.

Use the *Import info from JSON* button to import font info values from a `.json` file.

Edit the font info values in the list as needed.

Use the *select all attributes* checkbox to select/deselect all attributes in the list.

Use the *export to JSON file* button to save the <!--selected--> font info values to a `.json` file.

Click on the <em>apply selected info</em> button to apply the selected font info attributes to the selected fonts.

Select *preflight* to simulate the action before applying it.

### glyph set

![](/images/batch/BatchSet_2.png)

Use the *glyph set* to define a glyph set to apply to the selected fonts.

### unicodes

![](/images/batch/BatchSet_3.png)

Use the *unicodes* to set unicodes in the selected fonts.


set style data
--------------

...


find & replace info
-------------------

...
