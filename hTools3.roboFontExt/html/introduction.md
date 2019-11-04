Introduction
============

back to [index](index.html)

Interface
---------

hTools3 dialogs and scripts are accessible from the *hTools3* menu.

hTools3 documentation and settings are available from the *hTools3* entry in the RoboFont *Extensions* menu.

Toolsets
--------

hTools3 dialogs are organized around common patterns or scopes in font production tasks:

<dl>

<dt>batch
<dd>Tools to apply actions to multiple fonts at once in batch, without opening fonts in the interface.

<dt>font
<dd>Tools to apply actions which modify font-level data.

<dt>glyphs
<dd>Tools to apply actions to selected glyphs in the Font Overview and/or the current glyph in the Glyph Editor.

<dt>glyph
<dd>Tools to visualize and edit glyph data in the Glyph Editor.

<dt>proofing
<dd>Tools to generate different kinds of proofs for the current font.

</dl>

Extensions
----------

The hTools3 toolkit is packaged as one main [core extension][hTools3_core] containing the *font* and *glyphs* tools and reuseable modules, and optional additional extensions containing the [batch][hTools3_batch], [glyph][hTools3_glyph] and [proofing][hTools3_proofing] tools.

[hTools3_core]: http://gitlab.com/hipertipo/htools3_core_extension
[hTools3_batch]: http://gitlab.com/hipertipo/htools3_batch_extension
[hTools3_glyph]: http://gitlab.com/hipertipo/htools3_glyph_extension
[hTools3_proofing]: http://gitlab.com/hipertipo/htools3_proofing_extension
