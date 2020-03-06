Introduction
============

back to [index](index.html)

<!--
- [Interface](#interface)
- [Toolsets](#toolsets)
- [Extensions](#extensions)
- [Licensing](#licensing)
- [Support](#support)
-->


hTools3 is a rewrite of [hTools2] for RoboFont 3.

[hTools2]: http://github.com/gferreira/hTools2


Interface
---------

hTools3 dialogs and scripts are accessible from the *hTools3* menu.

hTools3 documentation and settings are available from the *hTools3* entry in the RoboFont *Extensions* menu.


Toolsets
--------

hTools3 dialogs are organized around common patterns or scopes in font production tasks:

<dl>

<dt>batch
<dd>Applying actions to multiple fonts at once in batch, without opening fonts in the interface.

<dt>font
<dd>Applying actions to modify font-level data.

<dt>glyphs
<dd>Applying actions to selected glyphs in the Font Overview and/or the current glyph in the Glyph Editor.

<dt>glyph
<dd>Visualizing and editing glyph data in the Glyph Editor.

<dt>proofing
<dd>Generating different kinds of proofs for the current font.

</dl>


Extensions
----------

The hTools3 toolkit is packaged as one [core extension][hTools3_core] containing the *font* and *glyphs* tools and reusable modules, and optional additional extensions containing the [batch][hTools3_batch], [glyph][hTools3_glyph] and [proofing][hTools3_proofing] tools.

<!--
| extension          | toolsets     |
|--------------------|--------------|
| [hTools3_core]     | font, glyphs |
| [hTools3_batch]    | batch        |
| [hTools3_glyph]    | glyph        |
| [hTools3_proofing] | proofing     |
-->

[hTools3_core]: http://gitlab.com/hipertipo/htools3_core_extension
[hTools3_batch]: http://gitlab.com/hipertipo/htools3_batch_extension
[hTools3_glyph]: http://gitlab.com/hipertipo/htools3_glyph_extension
[hTools3_proofing]: http://gitlab.com/hipertipo/htools3_proofing_extension


Licensing
---------

hTools3 is available from the [Extension Store] as compiled extensions.

The hTools3 source code is also available under open source license on request.

[Extension Store]: http://extensionstore.robofont.com/


Support
-------

- [hTools3 mailing list](#)
- [get in touch](mailto:gustavo@hipertipo.com)
